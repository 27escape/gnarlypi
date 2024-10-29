#!/usr/bin/env bash
# choose which displays to use and create the start_displays.sh script

DISPLAY_SCRIPT="./start_displays.sh"

# ----------------------------------------------------------------------------

function prompt_yn() {
  local msg=${1:-"Do you wish to proceed"}

  while true ; do
    read -p "$msg? (Y/N)" choice
    case "$choice" in
      y|Y ) return 0   ;;
      n|N ) return 1 ;;
      * ) echo "invalid answer, Y or N required";;
    esac
  done
}

# ----------------------------------------------------------------------------

clear
if [ ! -f "$DISPLAY_SCRIPT" ] || prompt_yn "Do you wish to update the display choices"  ; then
  echo "#!/usr/bin/bash
# reconfigure with the display_config.sh script,
# \$GNARLY_LOG comes from be_gnarly script
# do not modify by hand
  " > "$DISPLAY_SCRIPT"
  chmod a+x "$DISPLAY_SCRIPT"

  # "curses" and "basic" basic would need to be launched as an alternative
  # login program to display on the console, rather than the usual bash login

  for display in gnarly_status_*  ; do
    if prompt_yn "Do you wish to install $display" ; then
      echo "nohup \"./$display\" >> \$GNARLY_LOG 2>&1 &" >> "$DISPLAY_SCRIPT"
    fi
  done
fi


