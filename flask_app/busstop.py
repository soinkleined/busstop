'''standard module import'''
import time
import configparser
import math
import json
from datetime import datetime as dt
import pytz
import requests
import sys

CONFIG = configparser.ConfigParser(
            converters={'list': lambda x: [i.strip() for i in x.split(',')]})
CONFIG.read('config.ini')
URL = 'https://api.tfl.gov.uk/StopPoint/'
BACKOFF = 10
LOCAL_TZ = pytz.timezone('Europe/London')
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


def utc_to_local(utc_dt):
    '''convert time to proper format'''
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)


def get_tfl(tfl_id, timeout):
    '''download TFL json'''
    response = None
    retry_secs = 0
    while response is None:
        try:
            response = requests.get(URL + tfl_id, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            retry_secs += BACKOFF
            print('Exception ', err, file=sys.stderr, flush=True)
            print("Retrying in ", retry_secs,
                  " seconds.", file=sys.stderr, flush=True)
            time.sleep(retry_secs)
            response = None
    return response.json()


def get_stop_name(stop_id):
    '''parse busstop name'''
<<<<<<< HEAD
    json_result = get_tfl(stop_id,10)
    return json_result['commonName']
=======
    json_result = get_tfl(stop_id, 10)
    stop_name = json_result['commonName']
    return stop_name
>>>>>>> 0ba67ed (	modified:   Dockerfile - added debug)


def get_bus_time(stop_id, num_busses):
    '''format line schedule line data'''
    busses = []
    num = 0
    now = dt.now(LOCAL_TZ)
<<<<<<< HEAD
    json_result = get_tfl(f'{stop_id}/Arrivals', 10)
    json_result.sort(key = lambda x:x["expectedArrival"])
    stop_name=get_stop_name(stop_id)
    date_and_time = now.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
=======
    json_result = get_tfl(stop_id + '/Arrivals', 10)
    json_result.sort(key=lambda x: x["expectedArrival"])
    stop_name = get_stop_name(stop_id)
    date_and_time = now.strftime(DATE_FORMAT + " " + TIME_FORMAT)
>>>>>>> 0ba67ed (	modified:   Dockerfile - added debug)
    for item in json_result:
        due_in = None
        num += 1
        read_time = dt.strptime(item['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ")
        local_dt = utc_to_local(read_time)
<<<<<<< HEAD
        arrival_time=local_dt.strftime(TIME_FORMAT)
        away_min=math.floor(item['timeToStation']/60)
        due_in = 'due' if away_min == 0 else f'{str(away_min)}min'
        bus = {"number":str(num),
               "lineName":str(item['lineName']),
               "destinationName":str(item['destinationName']),
               "arrivalTime":arrival_time,
               "dueIn":due_in}
=======
        arrival_time = local_dt.strftime(TIME_FORMAT)
        away_min = math.floor(item['timeToStation']/60)
        if away_min == 0:
            due_in = 'due'
        else:
            due_in = str(away_min) + 'min'
        bus = {"number": str(num),
               "lineName": str(item['lineName']),
               "destinationName": str(item['destinationName']),
               "arrivalTime": arrival_time,
               "dueIn": due_in}
>>>>>>> 0ba67ed (	modified:   Dockerfile - added debug)
        busses.append(bus)
        if num == num_busses:
            break
    if num == 0:
        bus = {"noInfo": "No information at this time."}
        busses.append(bus)
<<<<<<< HEAD
    return {"stopName":stop_name ,"dateAndTime":date_and_time, "busses":busses}
=======
    my_stops = {"stopName": stop_name,
                "dateAndTime": date_and_time,
                "busses": busses}
    return my_stops
>>>>>>> 0ba67ed (	modified:   Dockerfile - added debug)


def get_stops():
<<<<<<< HEAD
    '''download stop information''' 
    all_stops=[]
    for num, stop_id in enumerate(CONFIG.getlist('busstop','stopid')):
        num_busses=int(CONFIG.getlist('busstop','num_busses')[num])
        all_stops.append(get_bus_time(stop_id,num_busses))
=======
    '''download stop information'''
    all_stops = []
    num = 0
    for stop_id in CONFIG.getlist('busstop', 'stopid'):
        num_busses = int(CONFIG.getlist('busstop', 'num_busses')[num])
        all_stops.append(get_bus_time(stop_id, num_busses))
        num += 1
>>>>>>> 0ba67ed (	modified:   Dockerfile - added debug)
    return all_stops


if __name__ == "__main__":
    print(json.dumps(get_stops(), indent=4))
