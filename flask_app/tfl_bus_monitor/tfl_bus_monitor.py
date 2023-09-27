"""standard package import"""
import configparser
import json
import logging
import math
import time
from datetime import datetime as dt
from logging import Formatter

import pytz
import requests



logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',  # Specify the log message format
    datefmt='%Y-%m-%d %H:%M:%S %z'  # Define the date format
)

logger = logging.getLogger(__name__)

class TFLBusMonitor:
    def __init__(self, config_file='config.ini'):
        self.CONFIG = configparser.ConfigParser(
            converters={'list': lambda x: [i.strip() for i in x.split(',')]})
        self.CONFIG.read(config_file)
        self.URL = 'https://api.tfl.gov.uk/StopPoint/'
        self.BACKOFF = 10
        self.LOCAL_TZ = pytz.timezone('Europe/London')
        self.DATE_FORMAT = "%Y-%m-%d"
        self.TIME_FORMAT = "%H:%M:%S"

    def utc_to_local(self, utc_dt):
        """convert time to proper format"""
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(self.LOCAL_TZ)

    def get_tfl(self, tfl_id, timeout):
        """download TFL json"""
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

    def get_stop_name(self, stop_id):
        """parse busstop name"""
        json_result = self.get_tfl(stop_id, 10)
        stop_name = json_result['commonName']
        return stop_name

    def get_bus_time(self, stop_id, num_busses):
        """format line schedule line data"""
        busses = []
        num = 0
        now = dt.now(self.LOCAL_TZ)
        json_result = self.get_tfl(stop_id + '/Arrivals', 10)
        json_result.sort(key=lambda x: x["expectedArrival"])
        stop_name = self.get_stop_name(stop_id)
        date_and_time = now.strftime(f"{self.DATE_FORMAT} {self.TIME_FORMAT}")
        for item in json_result:
            num += 1
            read_time = dt.strptime(item['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ")
            local_dt = self.utc_to_local(read_time)
            arrival_time = local_dt.strftime(self.TIME_FORMAT)
            away_min = math.floor(item['timeToStation'] / 60)
            due_in = 'due' if away_min == 0 else f'{str(away_min)}min'
            bus = {"number": str(num),
                   "lineName": str(item['lineName']),
                   "destinationName": str(item['destinationName']),
                   "arrivalTime": arrival_time,
                   "dueIn": due_in}
            busses.append(bus)
            if num == num_busses:
                break
        if num == 0:
            bus = {"noInfo": "No information at this time."}
            busses.append(bus)
        my_stops = {"stopName": stop_name,
                    "dateAndTime": date_and_time,
                    "busses": busses}
        return my_stops

    def get_stops(self):
        """download stop information"""
        all_stops = []
        num = 0
        for stop_id in self.CONFIG.getlist('busstop', 'stopid'):
            num_busses = int(self.CONFIG.getlist('busstop', 'num_busses')[num])
            all_stops.append(self.get_bus_time(stop_id, num_busses))
            num += 1
        return all_stops


if __name__ == "__main__":
    bus_monitor = TFLBusMonitor()
    print(json.dumps(bus_monitor.get_stops(), indent=4))
