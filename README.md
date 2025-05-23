<p align="center">
<img src="flask_app/static/ico/android-chrome-192x192.png" alt="busstop">
</p>
<h1 align="center" style="margin-top: 0px;">busstop</h1>
<p align="center" >Realtime London bus stop information from TFL, on a raspberry pi, on your desktop.</p>
<p align="center" >Now also supporting tube stops!</p>

# Info
Busstop returns current arrival information for busses and tube trains at the requested stop(s).  It prints the output in a style similar to that of the live bus and tube update signs available at many bus stops and stations throughout London.

The script runs as a flask application and uses turbo flask web sockets to update it dynamically in 15 second intervals. It is intended to run via a raspberry pi whilst using chrome in kiosk mode.

Originally, the idea was to use a pi zero, which worked, but as changes to Raspberry Pi OS  and chromium have made it more and more difficult to run kisok mode, the current release runs on a RPI 3, bookworm using wayland.

That being said, busstop should run on most system running python and often runs on my mac.

Clone the repo:

    git clone https://github.com/soinkleined/busstop.git
    cd busstop

Using the TFL API, find the corresponding StopPoint(s) and add it/them to the ~/busstop_config.ini file.  You can also configure the number of bussess to display per stop. By default, a config file will be installed in the config directory of the tfl_bus_monitor package.

Individual stopids can be found by looking for the arrivals at the stop via the TFL website.  For example:

https://tfl.gov.uk/bus/arrivals/490015396S/newington-green/

The stopid for Newington Green is 490015396S as can be seen in the URL above.  To download a reference for all stopids, TFL also makes this data available.

The column where the stopid is located is "Naptan_Atco" and you might want to validate it against the "Stop_Name":

http://tfl.gov.uk/tfl/syndication/feeds/bus-stops.csv

Here is an example configuration.  Use comma-separated stopids and values for the number of busses you'd like to display for each stop.  "0" will display all available busses.  Keep in mind your screen size and adjust appropriately. 

    [busstop]
    #Clissold Crescent, Newington Green
    stopid = 490005432S2,490015396S
    num_services=10,10

Install a python virtual environment and all requisite packages: 

    cd flask_app
    python -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

After cloning the repo and all requisite packages are installed, do the following:

    flask --app main run

Point your browser to http://127.0.0.1:5000/

There are also wrapper scripts to start the application with flask or gunicorn.

For running the application as a service for kiosk mode, there are systemd unit files in the kiosk_files folder that will have all the requisite configuration information for gunicorn, nginx, chrome, etc.

![busstop web](readme_images/busstop_web.png)

![busstop example](readme_images/busstop_example.jpeg)

# Hardware list
Some of these links are no longer valid or relevant.

Links to the hardware:
- pi zero wh https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414297171
- screen https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075
- case https://www.shapeways.com/product/QQ225Z4NP/case-for-hyperpixel-4-0-square-non-touch-pi-zero
- on/off usb switch https://thepihut.com/products/micro-usb-cable-with-on-off-switch

![hardware](readme_images/hardware.jpeg)

## Acknowledgements
Balena.io is a very interesting platform for IoT fleet management.  I saw their blog post about creating a live train time sign under your monitor and was inspired to do something similar for busses. There are a lot of links to other resources from the post as well as many other project ideas. 

https://www.balena.io/blog/build-a-raspberry-pi-powered-train-station-oled-sign-for-your-desk/

I used the fonts from Sean Petykowski and created webfonts via Font Squirrel. Thank you very much!

Please see the original ttf fonts here:

https://github.com/petykowski/London-Underground-Dot-Matrix-Typeface

and converted here:

https://www.fontsquirrel.com/tools/webfont-generator

Other useful links and acknowledgements:

https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask

https://jsonpathfinder.com/

https://github.com/realpython/flask-boilerplate

https://stackoverflow.com/questions/335695/lists-in-configparser

https://itecnote.com/tecnote/python-elegant-way-to-adjust-date-timezones-in-python/

https://trstringer.com/logging-flask-gunicorn-the-manageable-way/

https://github.com/celly/transparent-xcursor

<div>Icons made by <a href="https://www.flaticon.com/authors/mavadee" title="mavadee">mavadee</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

# License [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://raw.githubusercontent.com/soinkleined/busstop/main/LICENSE.md)
This project is licensed under the terms of the MIT license.

