import requests
import math
import json
import sys
from datetime import datetime as dt
from pytz import timezone
from termcolor import colored

'''
curl "https://api.tfl.gov.uk/StopPoint/490005432S2/Arrivals" | jq .
https://api.tfl.gov.uk/swagger/ui/index.html#!/StopPoint/StopPoint_MetaCategories
490015396S -> Newington Green
490005432S2 -> Clissold Crescent
'''

'''
https://pypi.org/project/termcolor/
Can be one of the following:
grey red green yellow blue magenta cyan white
or unset it: 
color = None
'''
color='yellow'
web=1

def getStopName(id):
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id)
    json_result = r.json()
    stop_name=json_result['commonName']
    return(stop_name)

def getBusTime(id):
    now = dt.now(timezone('Europe/London'))
    date_format = "%Y-%m-%d"
    time_format  = "%H:%M:%S"
    r = requests.get('https://api.tfl.gov.uk/StopPoint/' + id + '/Arrivals')
    json_result = r.json()
    json_result.sort(key = lambda x:x["expectedArrival"])
    my_stops = []
    if web:
        stop_name=getStopName(id)
        date_and_time = now.strftime(date_format  + " " + time_format)
        my_stops.append('        <span class="stop_name">' + stop_name + '</span></br>')
        my_stops.append('        <span class="date_and_time">' + date_and_time + '</span></br>')
    elif color:
        stop_name=colored(getStopName(id),color)
        date_and_time = colored(now.strftime(date_format  + " " + time_format), color) 
        my_stops.append(stop_name.center(62)) # termcolor adds characters
        my_stops.append(date_and_time.center(62))
    else:
        stop_name=getStopName(id)
        date_and_time = now.strftime(date_format  + " " + time_format) 
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
          if web:
              x =  '        <span class="number">' + str(num) + '</span><span class="lineName">' + str(x['lineName']) + '</span><span class="destinationName">' + str(x['destinationName']) + '</span><span class="arrival_time">' + arrival_time + '</span><span class="due_in">' + due_in + '</span></br>'
          elif color:
              x = colored("%3s %4s %30s %9s %6s" % (str(num),str(x['lineName']),str(x['destinationName']),arrival_time,due_in), color)
          else:
              x = "%3s %4s %30s %9s %6s" % (str(num),str(x['lineName']),str(x['destinationName']),arrival_time,due_in)
          my_stops.append(x)
    if num == 0:
        x = colored('No information at this time.',color)    
        my_stops.append(x)
    return(my_stops)

def printWeb(top_or_bottom):
    if top_or_bottom == 'top':
        print("""<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"
	\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">
<head>
	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
	<link rel=\"stylesheet\" href=\"css/font_stylesheet.css\" type=\"text/css\" charset=\"utf-8\" />
	<link rel=\"stylesheet\" href=\"css/stylesheet.css\" type=\"text/css\" charset=\"utf-8\" />
	<style type=\"text/css\">
					body{
				font-family: \"london_undergroundregular\";
							}
		</style>
	<title>busstop</title>
</head>
<body>
    <div id=\"container\">""")
    elif top_or_bottom == 'bottom':
        print("""    </div> 
</body>""")

def main(argv):
    if web:
        printWeb('top')
    for x in argv[1:]:
        for stop in(getBusTime(x)):
            print(stop)
        print()
    if web:
        printWeb('bottom')

if __name__ == "__main__":
    main(sys.argv)

'''
needs error checking and debugging
need to handle formatting better and add other formats, i.e. emoji, rendered image, etc
'''

