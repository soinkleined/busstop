<p align="center">
<img src="https://raw.githubusercontent.com/soinkleined/busstop/develop/flask_app/static/ico/android-chrome-192x192.png" alt="busstop">
</p>
<h1 align="center" style="margin-top: 0px;">busstop</h1>
<p align="center" >Realtime London bus stop information from TFL, on a raspberry pi, on your desktop.</p>

# Info
Busstop returns current arrival information for busses at the requested stop(s).  It prints the output in a style similar to that of the live bus update signs available at many bus stops throughout London.

The script runs as a flask appliction and uses turbo flask web sockets to update it dynamically in 15 second intervals. It is intended to run via a raspberry pi whilst using chrome in kiosk mode.

Clone the repo:

    git clone -b develop https://github.com/soinkleined/busstop.git
    cd busstop

Using the TFL API, find the corresponding StopPoint(s) and add it/them to the properties/config.ini file.  You can also configure the number of bussess to display per stop.

The column where the stopid is located is "Naptan_Atco" and you might want validate it against the "Stop_Name":

http://tfl.gov.uk/tfl/syndication/feeds/bus-stops.csv

Here is an example configuration.  Use comma-separated stopids and values for the number of busses you'd like to display for each stop.  "0" will display all available busses.  Keep in mind your screen size and adjust appropriately. 

    [busstop]
    #Newington Green, Clissold Crescent
    stopid = 490005432S2,490015396S
    num_busses=10,10

Install a python virtual environment and all requisite packages: 

    cd flask_app
    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

After cloning the repo and all requisite packages are installed, do the following:

    flask run

Point your browser to http://127.0.0.1:5000/

For running the appliation as a service for kiosk mode, there is a work in progress in the kiosk_files folder that will have all the requisite configuration information for guncorn, nginx, chrome, etc.

![busstop web](https://raw.githubusercontent.com/soinkleined/busstop/develop/readme_images/busstop_web.png)

![busstop example](https://raw.githubusercontent.com/soinkleined/busstop/develop/readme_images/busstop_example.jpeg)

# Hardware list
Links to the hardware:
- pi zero wh https://shop.pimoroni.com/products/raspberry-pi-zero-w?variant=39458414297171
- screen https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075
- case https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075
- on/off usb switch https://thepihut.com/products/micro-usb-cable-with-on-off-switch

![hardware](https://raw.githubusercontent.com/soinkleined/busstop/develop/readme_images/hardware.jpeg)

# To Do
1. add any missing credits
2. finish kiosk build automation
3. handle errors for connectivity, api availability, etc.
4. look for confg optimisations for RPI zero, i.e. zram, gpu memory config, etc
5. do i need nginx in front of gunicorn on an rpi zero?

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

<div>Icons made by <a href="https://www.flaticon.com/authors/mavadee" title="mavadee">mavadee</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

# License [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://raw.githubusercontent.com/soinkleined/busstop/develop/LICENSE.md)
This project is licensed under the terms of the MIT license.
