"""
standard package import
"""
import configparser
import logging
import os
import time
import math
import json
import importlib.resources as resources
from datetime import datetime as dt
from typing import Any, List, Dict, Union

import pytz
import requests

logging.basicConfig(
    format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)

logger = logging.getLogger(__name__)
logger.propagate = False

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logger.setLevel(gunicorn_logger.level)


def get_config_path() -> str:
    """Return path to config file"""
    conf_file_name = "busstop_config.ini"
    if "BUSSTOP_HOME" in os.environ:
        return os.environ[f"BUSSTOP_HOME/{conf_file_name}"]
    home_dir = os.path.expanduser("~")
    if os.path.isfile(f"{home_dir}/{conf_file_name}"):
        return f"{home_dir}/{conf_file_name}"
    package_path = resources.files(__package__)
    return os.path.join(str(package_path), f"config/{conf_file_name}")


class TFLBusMonitor:
    """Provide stop information as json or text """
    def __init__(self) -> None:
        self.CONFIG = configparser.ConfigParser(
            converters={'list': lambda x: [i.strip() for i in x.split(',')]})
        self.stop_name_cache: Dict[str, str] = {}
        self.CONFIG_FILE: str = get_config_path()
        self.URL: str = 'https://api.tfl.gov.uk/StopPoint/'
        self.BACKOFF: int = 10
        self.LOCAL_TZ = pytz.timezone('Europe/London')
        self.DATE_FORMAT: str = "%Y-%m-%d"
        self.TIME_FORMAT: str = "%H:%M:%S"

    def utc_to_local(self, utc_dt: dt) -> dt:
        """Convert UTC time to local time"""
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(self.LOCAL_TZ)

    def get_tfl(self, tfl_id: str, timeout: int) -> Union[Dict[str, Any], None]:
        """Download TFL JSON data"""
        response = None
        retry_secs = 0
        error_info = None  # Store error information

        while response is None:
            try:
                response = requests.get(self.URL + tfl_id, timeout=timeout)
                response.raise_for_status()
                retry_secs = 0
            except requests.exceptions.ConnectionError as conn_err:
                error_info = {"error_type": "ConnectionError", "message": str(conn_err)}
                retry_secs += self.BACKOFF
                response = None
            except requests.exceptions.Timeout as timeout_err:
                error_info = {"error_type": "Timeout", "message": str(timeout_err)}
                retry_secs += self.BACKOFF
                response = None
            except requests.exceptions.HTTPError as http_err:
                error_info = {"error_type": "HTTPError", "message": str(http_err)}
                retry_secs += self.BACKOFF
                response = None
            except requests.exceptions.RequestException as req_err:
                error_info = {"error_type": "RequestException", "message": str(req_err)}
                retry_secs += self.BACKOFF
                response = None

            if response is None:
                logger.error(f"{error_info['error_type']}")
                logger.error(f"{error_info['message']}")
                logger.error(f"Retrying in {retry_secs} seconds.")
                time.sleep(retry_secs)
        logger.info(f"{response.status_code} {response.reason} -> {self.URL}{tfl_id}")
        return response.json() if response else None

    def get_stop_name(self, stop_id: str) -> str:
        """Parse bus stop name"""
        if stop_id in self.stop_name_cache:
            return self.stop_name_cache[stop_id]
        json_result = self.get_tfl(stop_id, 10)
        stop_name = json_result['commonName']

        if stop_name:
            self.stop_name_cache[stop_id] = stop_name  # Cache the stop name

        return stop_name

    def get_bus_time(self, stop_id: str, num_busses: int) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """Format bus schedule data"""
        busses = []
        num = 0
        now = dt.now(self.LOCAL_TZ)
        json_result = self.get_tfl(f"{stop_id}/Arrivals", 10)
        if json_result is not None and isinstance(json_result, list):
            json_result.sort(key=lambda x: x["expectedArrival"])
        stop_name = self.get_stop_name(stop_id)
        date_and_time = now.strftime(f"{self.DATE_FORMAT} {self.TIME_FORMAT}")
        for item in json_result:
            num += 1
            read_time = dt.strptime(item['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ")
            local_dt = self.utc_to_local(read_time)
            arrival_time = local_dt.strftime(self.TIME_FORMAT)
            away_min = math.floor(int(item['timeToStation']) / 60)
            due_in = 'due' if away_min == 0 else f'{str(away_min)}min'
            bus_info = {"number": str(num),
                        "lineName": str(item['lineName']),
                        "destinationName": str(item['destinationName']),
                        "arrivalTime": arrival_time,
                        "dueIn": due_in}
            busses.append(bus_info)
            if num == num_busses:
                break
        if num == 0:
            bus_info = {"noInfo": "No information at this time."}
            busses.append(bus_info)
        return {
            "stopName": stop_name,
            "dateAndTime": date_and_time,
            "busses": busses,
        }

    def get_stops(self) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """Download stop information"""
        all_stops = []
        self.CONFIG.read(self.CONFIG_FILE)
        for num, stop_id in enumerate(self.CONFIG.getlist('busstop', 'stopid')):
            num_busses = int(self.CONFIG.getlist('busstop', 'num_busses')[num])
            all_stops.append(self.get_bus_time(stop_id, num_busses))
        return all_stops


def main() -> None:
    """Main entry point"""
    import argparse

    bus_monitor = TFLBusMonitor()
    bus_json = bus_monitor.get_stops()

    def print_json(busstop_json: List[Dict[str, Union[str, List[Dict[str, str]]]]]) -> None:
        """Pretty print JSON"""
        print(json.dumps(busstop_json, indent=4))

    def print_text(busstop_json: List[Dict[str, Union[str, List[Dict[str, str]]]]]) -> None:
        """Print formatted text"""
        for stop in busstop_json:
            align = math.ceil((76 + len(stop['stopName'])) / 2)
            print(f"\033[1;33;40m{stop['stopName']:>{align}}\033[0m")
            for bus in stop['busses']:
                if 'noInfo' in bus:
                    print(f"\033[1;33;40m{bus['noInfo']}\033[0m")
                else:
                    print(
                        f"\033[0;33;40m{bus['number']:3} {bus['lineName']:5} {bus['destinationName']:50} "
                        f"{bus['arrivalTime']:9} {bus['dueIn']:>6}\033[0m"
                    )
            print("\n")

    def formatter(prog: str) -> argparse.HelpFormatter:
        """Format help output instead of lambda function"""
        return argparse.HelpFormatter(prog, max_help_position=100, width=200)

    description = "Get bus stop data from TFL"
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--print-text', action='store_true', help='print formatted text')
    group.add_argument('-j', '--print-json', action='store_true', help='pretty print json (default)')
    args = parser.parse_args()

    if args.print_text:
        print_text(bus_json)
    else:
        print_json(bus_json)


if __name__ == "__main__":
    main()
