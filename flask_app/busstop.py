import requests
import math
import json
import sys
from datetime import datetime as dt
import pytz
import configparser
import os
import time

config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read(os.path.join('../properties', 'config.ini'))
url = 'https://api.tfl.gov.uk/StopPoint/'
backoff = 10
local_tz=pytz.timezone('Europe/London')

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

def getTFL(id,timeout):
    r = False
    retry_secs = 0
    while not r:
        time.sleep(retry_secs)
        try:
            r = requests.get(url + id,timeout=timeout)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Exception:",err)
        retry_secs += backoff
    return(r.json())

def getStopName(id):
    json_result = getTFL(id,10)
    stop_name=json_result['commonName']
    return(stop_name)

def getBusTime(id,num_busses):
    busses=[]
    num = 0
    now = dt.now(local_tz)
    date_format = "%Y-%m-%d"
    time_format  = "%H:%M:%S"
    json_result = getTFL(id + '/Arrivals',10)
    json_result.sort(key = lambda x:x["expectedArrival"])
    stop_name=getStopName(id)
    date_and_time = now.strftime(date_format  + " " + time_format) 
    for x in json_result:
          due_in=None
          num += 1
          read_time=dt.strptime(x['expectedArrival'],"%Y-%m-%dT%H:%M:%SZ")
          local_dt = utc_to_local(read_time)
          arrival_time=local_dt.strftime(time_format)
          away_min=math.floor(x['timeToStation']/60)
          if away_min == 0:
              due_in = 'due'
          else:
              due_in = str(away_min) + 'min'
          bus = {"number":str(num),"lineName":str(x['lineName']),"destinationName":str(x['destinationName']),"arrivalTime":arrival_time,"dueIn":due_in}
          busses.append(bus)
          if num == num_busses:
                  break
    if num == 0:
        bus = {"noInfo":"No information at this time."}    
        busses.append(bus)
    my_stops ={"stopName":stop_name ,"dateAndTime":date_and_time, "busses":busses}
    return(my_stops)

def getStops():
    all_stops=[]
    num=0
    for id in config.getlist('busstop','stopid'):
        num_busses=int(config.getlist('busstop','num_busses')[num])
        all_stops.append(getBusTime(id,num_busses))
        num+=1
    return(all_stops)


if __name__ == "__main__":
   print(json.dumps(getStops(), indent=4))
