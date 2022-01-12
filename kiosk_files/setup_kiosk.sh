##############################
# Vars
##############################
NEW_HOSTNAME='busstop'
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
TIMESTAMP=$(date +%Y%m%d%H%M%S)
AUTOSTART="/etc/xdg/lxsession/LXDE-pi/autostart"
SPLASH="/usr/share/plymouth/themes/pix/splash.png"

##############################
# Set browser kiosk startup
##############################
mv  "${AUTOSTART}" "${AUTOSTART}.${TIMESTAMP}"

echo "# Configured by busstop on ${TIMESTAMP}
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xset s off
@xset -dpms
@xset s noblank" > "${AUTOSTART}"

##############################
# Set splash screen
##############################
mv "${SPLASH}" "${SPLASH}.${TIMESTAMP}"
cp ./splash.png "${SPLASH}"

##############################
# Set hostname
##############################
cp /etc/hostname "/etc/hostname.${TIMESTAMP}"
cp /etc/hosts "/etc/hosts.${TIMESTAMP}"
echo $NEW_HOSTNAME > /etc/hostname
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts
