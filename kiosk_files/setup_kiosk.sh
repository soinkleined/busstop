#!/bin/env bash
##############################
# Vars
##############################
NEW_HOSTNAME='busstop'
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
TIMESTAMP=$(date +%Y%m%d%H%M%S)
AUTOSTART="/etc/xdg/lxsession/LXDE-pi/autostart"
SPLASH="/usr/share/plymouth/themes/pix/splash.png"
DIR=$(dirname "${0}")
echo $DIR && exit

##############################
# update OS and install software
##############################
sudo apt update
sudo apt full-upgrade
sudo apt install -y git xserver-xorg x11-xserver-utils xinit openbox chromium-browser unclutter nginx realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced

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
cp "${DIR}/images/splash.png" "${SPLASH}"

##############################
# Set hostname
##############################
cp /etc/hostname "/etc/hostname.${TIMESTAMP}"
cp /etc/hosts "/etc/hosts.${TIMESTAMP}"
echo $NEW_HOSTNAME > /etc/hostname
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts

##############################
# Configure busstop_server
##############################

sudo systemctl daemon-reload
sudo systemctl enable busstop_server
##############################
# Configure busstop_client
##############################

sudo systemctl enable busstop_client
##############################
# Configure nginx
##############################

sudo systemctl enable nginx
##############################
# Tweaks and Optimisations
##############################
#Disable hdmi to save power
#Configure usb as network interface for ssh (gadget mode)
