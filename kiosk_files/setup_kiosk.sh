TIMESTAMP=$(date +%Y%m%d%H%M%S)
AUTOSTART="/etc/xdg/lxsession/LXDE-pi/autostart"
SPLASH="/usr/share/plymouth/themes/pix/splash.png"
mv  "${AUTOSTART}" "${AUTOSTART}.${TIMESTAMP}"

echo "# Configured by busstop on ${TIMESTAMP}
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xset s off
@xset -dpms
@xset s noblank

@/home/pi/busstop/kiosk_files/run_busstop_browser.sh" > "${AUTOSTART}"

mv "${SPLASH}" "${SPLASH}.${TIMESTAMP}"
cp ./splash.png "${SPLASH}"
