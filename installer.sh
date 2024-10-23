#!/usr/bin/bash
# ----------------------------------------------------------------------------
# the assumption is that this script is going to be run on a system that will
# likely only be used for the gnarlypi application
# it uses a lot of python modules from various vendors to control displays
# it is the expectation of a lot of these vendors that the modules can be
# installed via apt as part of 'system python' and that they would not be installed
# with pip. Some of these modules do not work well either with 64-bit versions
# of the raspberry pi OS or are not up to date with the git repos and hence do not
# work. For python modules that are not part of the system (debian 12), it is
#  expected that the use would create a python virtual environment for each application
# where the need to use different modules.
# This can get messy if doing this for multiple things
# the alternative, suggested by Jeff Geerling is to remove a global file
# that will prevent the system python from complaining when we do things
# and this is fine on a raspberry pi where there is only one user and
# we may(!) know what we are doing


REBOOT_REQUIRED=0
FIRMWARE_FILE="/boot/firmware/config.txt"
SPI_OVERLAY="dtoverlay=spi0-0cs"
SAMBA_CFG="/etc/samba/smb.conf"
SAMBA_ORIG="$SMB_CFG.orig"

# ----------------------------------------------------------------------------
#  the standard upgrade
function system_upgrade() {
    sudo apt update && sudo apt upgrade -y
}

# ----------------------------------------------------------------------------
# install tools that we will likely require
function install_tools() {
    sudo apt install -y git jq build-essential python3-pip cmake mosquitto mosquitto-clients
}

# ----------------------------------------------------------------------------
# lets us use pip3 to install things
function override_system_python() {

  if [ -f "/usr/lib/python3.11/EXTERNALLY-MANAGED" ] ; then
    sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
  fi
}


# ----------------------------------------------------------------------------
function install_device_blinkt() {
  # this should work, I may have broke my blinkt!

    echo "Installing Blinkt!"
    # 0 means ON
    sudo raspi-config nonint do_i2c 0
    sudo apt remove -y python3-rpi.gpio
    pip3 install rpi-lgpio blinkt numphy
}

# ----------------------------------------------------------------------------
function install_device_ledshim() {
    echo "Installing ledshim"
    # 0 means ON
    sudo raspi-config nonint do_i2c 0
    sudo raspi-config nonint do_spi 0
    sudo apt remove -y python3-rpi.gpio

    pip3 install smbus ledshim numphy rpi-lgpio
}

# ----------------------------------------------------------------------------
function install_device_mini_pitft() {
    echo "Installing mini_pitft"
    # 0 means ON
    sudo raspi-config nonint do_i2c 0
    sudo raspi-config nonint do_spi 0
    sudo apt-get install fonts-dejavu -y
    pip3 install --upgrade adafruit-python-shell click
    pip3 install adafruit-circuitpython-rgb-display numphy pillow rpi-lgpio
  grep -q "$SPI_OVERLAY" "$FIRMWARE_FILE"
  if [ "$?" == "1" ] ; then
    REBOOT_REQUIRED=1
      echo "# gnarly pi enabling tis for the mini PiTFT display" >> $FIRMWARE_FILE
      sudo echo "$SPI_OVERLAY" >> $FIRMWARE_FILE
  fi
}

function install_samba() {
   echo "Installing Samba"
    smbconf="
# taken from the Sample configuration file for the Samba suite for Debian GNU/Linux.

#======================= Global Settings =======================

[global]
   workgroup = WORKGROUP

   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d

   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
   pam password change = yes
   map to guest = bad user

#======================= Share Definitions =======================


# just one share and user
[PHOTOS]
  valid users = $USER
  path = /home/$USER/usb_data
  writeable = yes
  browseable = yes
  create mask = 0777
  directory mask = 0777
  public = no
  veto files = /._*/.DS_Store/
  delete veto files = yes
"

  sudo apt install -y samba samba-common-bin

  # create samba user for current linux user
  sudo smbpasswd -a "$USER"

  if [ ! -f "$SAMBA_ORIG" ] ; then
    sudo cp $SAMBA_CFG "$SAMBA_CFG.orig"
    echo "$smbconf" | sudo tee "$SAMBA_CFG" > /dev/null

    sudo systemctl restart smbd
  else
    echo "smb.conf has previously been created, I will sample config in /tmp/smb.conf"
    echo "$smbconf" > "/tmp/smb.conf"
  fi

}


# ----------------------------------------------------------------------------
# install be_gnarly into crontab
function install_crontab() {

  TMP=$(mktemp)

  # test if we already have a crontab file, as if we are doing this from scratch
  # crontab -l may fail as it wants to setup an editor first :(

  if [ $(sudo ls "/var/spool/cron/crontabs/kevinmu" 2>/dev/null) == "0" ] ; then
    echo "" > "$TMP"
  else
    crontab -l > "$TMP"
  fi
  grep -q "gnalypi" "$TMP"
  if [ "$?" == "1" ] ; then
      echo "installing reboot rule into crontab"
      echo "#start gnarlypi on bootup
@reboot /home/$USER/gnarlypi/be_gnarly" >> "$TMP"
      # update crontab
      crontab "$TMP"
      rm "$TMP"
      echo "be_gnarly installed into your crontab, should start on next reboot"
  else
    echo "you are already gnarly enough!"
  fi
}

# ----------------------------------------------------------------------------
function install_gnarly() {
  echo "Installing gnarly code"
  pip3 install -r requirements.txt
}

# ----------------------------------------------------------------------------

system_upgrade
override_system_python
install_tools

install_crontab

install_device_blinkt
install_device_ledshim
install_device_mini_pitft
install_samba
install_gnarly

./display_config.sh

if [ "$REBOOT_REQUIRED" == "1" ] ; then
  echo "rebooting"
  sudo reboot
fi
