import requests
import math
import json
from datetime import datetime as dt
from pytz import timezone
from termcolor import colored

'''
curl "https://api.tfl.gov.uk/StopPoint/490005432S2/Arrivals" | jq .
https://api.tfl.gov.uk/swagger/ui/index.html#!/StopPoint/StopPoint_MetaCategories
490015396S -> Newington Green
490005432S2 -> Clissold Crescent
'''
debug = 0

def getStopName(id):
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id)
    json_result = r.json()
    stop_name=json_result['commonName']
    return(stop_name)
    if debug ==1:
        print(json.dumps(json_result, indent=4, sort_keys=True))

def getBusTime(id):
    now = dt.now(timezone('Europe/London'))
    date_format = "%Y-%m-%d"
    time_format  = "%H:%M:%S"
    date_and_time = now.strftime(date_format  + " " + time_format) 
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id + '/Arrivals')
    json_result = r.json()
    json_result.sort(key = lambda x:x["expectedArrival"])
    stop_name=getStopName(id)
    my_stops = []
    my_stops.append(stop_name.center(56))
    my_stops.append(date_and_time.center(56))
    num = 0
    for x in json_result:
          due_in=''
          num += 1
          read_time=dt.strptime(x['expectedArrival'],"%Y-%m-%dT%H:%M:%SZ")
          arrival_time=read_time.strftime(time_format)
          away_min=math.floor(x['timeToStation']/60)
          if away_min == 0:
              due_in = 'due'
          else:
              due_in = str(away_min) + 'min'
          x = "%3s %4s %30s %9s %6s" % (str(num),str(x['lineName']),str(x['destinationName']),arrival_time,due_in)
          my_stops.append(x)
    if num == 0:
        x = 'No information at this time.'    
        my_stops.append(x)
    for stop in my_stops:
        print(colored(stop, 'yellow'))
    if debug ==1:
        print(json.dumps(json_result, indent=4, sort_keys=True))

getBusTime('490005432S2')
print('\n')
getBusTime('490015396S')
print('\n')
