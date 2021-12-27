<p align="center">
<img src="https://raw.githubusercontent.com/soinkleined/busstop/develop/flask_app/static/ico/android-chrome-192x192.png" alt="busstop">
</p>
<h1 align="center" style="margin-top: 0px;">busstop</h1>
<p align="center" >Realtime London bus stop information from TFL, on a raspberry pi, on your desktop.</p>

# Info
Busstop returns current arrival information for busses at the requested stop(s).  It prints the output in a style similar to that of the live bus update signs available at many bus stops throughout London.

Using the TFL API, find the corresponding StopPoint(s) and provide it/them as (an) argument(s) to the script as follows:

`% python busstop.py  490015396S`

![busstop](https://raw.githubusercontent.com/soinkleined/busstop/develop/readme_images/busstop.png)

The script now also renders html output including dot matrix style webfonts.

![busstop web](https://raw.githubusercontent.com/soinkleined/busstop/develop/readme_images/busstop_web.png)

# To Do
1. optimize css code
2. add licenses and missing credits
3. setup on rpi with chromium kiosk mode
4. add better handling of formatting arguments
5. handle errors for connectivity, api availability, etc.

## Acknowledgements
Balena.io is a very interesting platform for IoT fleet management.  I saw their blog post about creating a live train time sign under your monitor and was inspired to do something similar for busses. There are a lot of links to other resources from the post and I hope to also do this from a pi zero with a custom case at some point.

https://www.balena.io/blog/build-a-raspberry-pi-powered-train-station-oled-sign-for-your-desk/

I used the fonts from Sean Petykowski and created webfonts via Font Squirrel. Thank you very much!

Please see the original ttf fonts here:

https://github.com/petykowski/London-Underground-Dot-Matrix-Typeface

and converted here:

https://www.fontsquirrel.com/tools/webfont-generator

Other useful links and acknowledgements:

https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask

https://www.shapeways.com/product/QQ225Z4NP/case-for-hyperpixel-4-0-square-non-touch-pi-zero

https://jsonpathfinder.com/

<div>Icons made by <a href="https://www.flaticon.com/authors/mavadee" title="mavadee">mavadee</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

