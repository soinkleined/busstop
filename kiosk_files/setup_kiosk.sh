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

##############################
# update OS and install software
##############################
sudo apt update
sudo apt full-upgrade
sudo apt install -y git xserver-xorg x11-xserver-utils xinit openbox chromium-browser unclutter nginx realvnc-vnc-server at-spi2-core
# at-spi2-core -> https://forums.raspberrypi.com/viewtopic.php?t=196070
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
# Configure services
##############################
sudo cp "${DIR}/service_configs/busstop_server.service" /etc/systemd/system/
sudo cp "${DIR}/service_configs/busstop_client.service" /etc/systemd/system/
sudo cp "${DIR}/service_configs/nginx.conf" /etc/nginx/sites-available/default
sudo systemctl daemon-reload
sudo systemctl enable busstop_server
sudo systemctl enable busstop_client
sudo systemctl enable nginx

##############################
# Tweaks and Optimisations
##############################
#Disable hdmi to save power
sudo sed /etc/rc.local -i -e "s/^exit 0/\/usr\/bin\/tvservice -o\nexit 0/"
#Configure usb as network interface for ssh (gadget mode)
grep ^dtoverlay=dwc2 /boot/config.txt || echo dtoverlay=dwc2 | sudo tee -a  /boot/config.txt
grep modules-load=dwc2,g_ether /boot/cmdline.txt || sudo sed /boot/cmdline.txt -i -e "s/rootwait/rootwait modules-load=dwc2,g_ether/"
#Setup autologin for the pi user
grep ^autologin-user=pi /etc/lightdm/lightdm.conf || sudo sed /etc/lightdm/lightdm.conf -i -e "s/^#autologin-user=.*/autologin-user=pi/"

