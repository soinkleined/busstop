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
url = 'https://api.tfl.gov.uk/StopPoint/'

def getStopName(id):
    try:
        r = requests.get(url + id,timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Exception:",err)
    json_result = r.json()
    stop_name=json_result['commonName']
    return(stop_name)

def getBusTime(id,num_busses):
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
'''
needs error checking and debugging
need to handle formatting better and add other formats, i.e. emoji, rendered image, etc
'''
