import requests
import math
import json
import sys
from datetime import datetime as dt
from pytz import timezone
import configparser
import os

'''
curl "https://api.tfl.gov.uk/StopPoint/490005432S2/Arrivals" | jq .
https://api.tfl.gov.uk/swagger/ui/index.html#!/StopPoint/StopPoint_MetaCategories
490015396S -> Newington Green
490005432S2 -> Clissold Crescent
'''

'''
https://stackoverflow.com/questions/335695/lists-in-configparser
'''
config = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config.read(os.path.join('../properties', 'config.ini'))

def getStopName(id):
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id)
    json_result = r.json()
    stop_name=json_result['commonName']
    return(stop_name)

def getBusTime(id):
    busses=[]
    num = 0
    now = dt.now(timezone('Europe/London'))
    date_format = "%Y-%m-%d"
    time_format  = "%H:%M:%S"
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id + '/Arrivals')
    json_result = r.json()
    json_result.sort(key = lambda x:x["expectedArrival"])
    stop_name=getStopName(id)
    date_and_time = now.strftime(date_format  + " " + time_format) 
    for x in json_result:
          due_in=None
          num += 1
          read_time=dt.strptime(x['expectedArrival'],"%Y-%m-%dT%H:%M:%SZ")
          arrival_time=read_time.strftime(time_format)
          away_min=math.floor(x['timeToStation']/60)
          if away_min == 0:
              due_in = 'due'
          else:
              due_in = str(away_min) + 'min'
          bus = {"number":str(num),"lineName":str(x['lineName']),"destinationName":str(x['destinationName']),"arrivalTime":arrival_time,"dueIn":due_in}
          busses.append(bus)
    if num == 0:
        bus = {"noInfo":"No information at this time."}    
        busses.append(bus)
    my_stops ={"stopName":stop_name ,"dateAndTime":date_and_time, "busses":busses}
    return(my_stops)

def getStops():
    all_stops=[]
    for x in config.getlist('busstop','stopid'):
        all_stops.append(getBusTime(x))
    return(all_stops)

'''
needs error checking and debugging
need to handle formatting better and add other formats, i.e. emoji, rendered image, etc
'''
