#!/usr/bin/env bash
#  this script will be sourced by other scripts
# ----------------------------------------------------------------------------

# for your user, create an entry in your crontab
# @reboot /home/$USER/gnarlypi/be_gnarly

# ----------------------------------------------------------------------------

export FULL_PATH="$HOME/gnarlypi"
export GNARLY_ERR_LOG="/tmp/gnarlypi.err"
export BIN_PATH=$FULL_PATH/bin
export GNARLYPI_CONFIG=$HOME/gnarlypi/gnarlypi.yml

# need to set this so python knows where the libraries are
export PYTHONPATH="$FULL_PATH:$PYTHONPATH"
