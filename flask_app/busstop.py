'''standard module import'''
import os
import time
import configparser
import math
import json
from datetime import datetime as dt
import pytz
import requests

CONFIG = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
CONFIG.read('config.ini')
URL = 'https://api.tfl.gov.uk/StopPoint/'
BACKOFF = 10
LOCAL_TZ=pytz.timezone('Europe/London')
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

def utc_to_local(utc_dt):
    '''convert time to proper format'''
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)

def get_tfl(tfl_id,timeout):
    '''download TFL json'''
    request = False
    retry_secs = 0
    while not request:
        if retry_secs != 0:
            print ("Retrying in ",retry_secs," seconds.")
        time.sleep(retry_secs)
        retry_secs += BACKOFF
        try:
            request = requests.get(URL + tfl_id,timeout=timeout)
            request.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("Exception:",  err)
    return request.json()

def get_stop_name(stop_id):
    '''parse busstop name'''
    json_result = get_tfl(stop_id,10)
    return json_result['commonName']

def get_bus_time(stop_id,num_busses):
    '''format line schedule line data'''
    busses=[]
    num = 0
    now = dt.now(LOCAL_TZ)
    json_result = get_tfl(f'{stop_id}/Arrivals', 10)
    json_result.sort(key = lambda x:x["expectedArrival"])
    stop_name=get_stop_name(stop_id)
    date_and_time = now.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
    for item in json_result:
        due_in=None
        num += 1
        read_time=dt.strptime(item['expectedArrival'],"%Y-%m-%dT%H:%M:%SZ")
        local_dt = utc_to_local(read_time)
        arrival_time=local_dt.strftime(TIME_FORMAT)
        away_min=math.floor(item['timeToStation']/60)
        due_in = 'due' if away_min == 0 else f'{str(away_min)}min'
        bus = {"number":str(num),
               "lineName":str(item['lineName']),
               "destinationName":str(item['destinationName']),
               "arrivalTime":arrival_time,
               "dueIn":due_in}
        busses.append(bus)
        if num == num_busses:
            break
    if num == 0:
        bus = {"noInfo":"No information at this time."}
        busses.append(bus)
    return {"stopName":stop_name ,"dateAndTime":date_and_time, "busses":busses}

def get_stops():
    '''download stop information''' 
    all_stops=[]
    for num, stop_id in enumerate(CONFIG.getlist('busstop','stopid')):
        num_busses=int(CONFIG.getlist('busstop','num_busses')[num])
        all_stops.append(get_bus_time(stop_id,num_busses))
    return all_stops


if __name__ == "__main__":
    print(json.dumps(get_stops(), indent=4))
