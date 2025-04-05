#!/bin/env bash
##############################
# Vars
##############################
NEW_HOSTNAME='busstop'
TIMESTAMP=$(date +%Y%m%d%H%M%S)
AUTOSTART="/etc/xdg/lxsession/LXDE-pi/autostart"
SPLASH="/usr/share/plymouth/themes/pix/splash.png"
DIR=$(dirname "${0}")

##############################
# update OS and install software
##############################
sudo apt update
sudo apt install -y nginx
sudo apt full-upgrade

##############################
# Set browser kiosk startup
##############################
sudo mv  "${AUTOSTART}" "${AUTOSTART}.${TIMESTAMP}"

echo "# Configured by busstop on ${TIMESTAMP}
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xset s off
@xset -dpms
@xset s noblank" | sudo tee "${AUTOSTART}"

##############################
# Set splash screen and background
##############################
sudo mv "${SPLASH}" "${SPLASH}.${TIMESTAMP}"
sudo cp "${DIR}/images/splash.png" "${SPLASH}"
echo "[*]
desktop_bg=#FFFFFF
desktop_shadow=#FFFFFF
desktop_fg=#000000
desktop_font=PibotoLt 12
wallpaper=${SPLASH}
wallpaper_mode=center
show_documents=0
show_trash=0
show_mounts=0
folder=/home/${USER}/Desktop" > /home/${USER}/.config/pcmanfm/LXDE-pi/desktop-items-DPI-1.conf

##############################
# Set hostname
##############################
if [ "${HOSTNAME}" = ${NEW_HOSTNAME} ]; then
    printf '%s\n' "Hostname is already set to ${NEW_HOSTNAME}."
else
    printf '%s\n' "Setting hostname from $HOSTNAME to ${NEW_HOSTNAME}."
    sudo cp /etc/hostname "/etc/hostname.${TIMESTAMP}"
    sudo cp /etc/hosts "/etc/hosts.${TIMESTAMP}"
    sudo echo ${NEW_HOSTNAME} > /etc/hostname
    sudo sed -i "s/127.0.1.1.*${HOSTNAME}/127.0.1.1\t${NEW_HOSTNAME}/g" /etc/hosts
fi

##############################
# setup nginx permissions and directory
##############################
chmod 755 /home/${USER}
sed "${DIR}/service_configs/nginx.conf" -i -e "s/USER/${USER}/"
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
# Configure Hyperpixel LCD
##############################
grep 'dtoverlay=vc4-kms-dpi-hyperpixel4sq' /boot/firmware/config.txt || echo dtoverlay=vc4-kms-dpi-hyperpixel4sq | sudo tee -a /boot/firmware/config.txt

##############################
# Hack to remove cursor - https://github.com/celly/transparent-xcursor/blob/master/transparent
##############################
sudo mv /usr/share/icons/PiXflat/cursors/left_ptr /usr/share/icons/PiXflat/cursors/left_ptr.${TIMESTAMP}
sudo mv /usr/share/icons/PiXflat/cursors/text /usr/share/icons/PiXflat/cursors/text.${TIMESTAMP}
sudo cp "${DIR}/cursor/transparent" /usr/share/icons/PiXflat/cursors/left_ptr
sudo cp "${DIR}/cursor/transparent" /usr/share/icons/PiXflat/cursors/text

