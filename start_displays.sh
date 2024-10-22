#!/usr/bin/bash
# reconfigure with the display_config.sh script,
# $GNARLY_LOG comes from be_gnarly script
# do not modify by hand
  
nohup "./gnarly_status_pitft" >> $GNARLY_LOG 2>&1 &
