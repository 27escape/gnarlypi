#!/usr/bin/env bash
# choose which displays to use and create the start_displays.sh script

FULL_PATH="$HOME/gnarlypi"
cd "$FULL_PATH" || (echo "cannot find dir $FULL_PATH" && exit 1)

DISPLAY_SCRIPT="$FULL_PATH/bin/start_displays.sh"
STATUS_DIR="$FULL_PATH/status"

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
# do not modify by hand
GNARLY_LOG='/tmp/gnarlypi-status.log'
cd '$STATUS_DIR'
" > "$DISPLAY_SCRIPT"
  chmod a+x "$DISPLAY_SCRIPT"

  # "curses" and "basic" basic would need to be launched as an alternative
  # login program to display on the console, rather than the usual bash login

  for display in status/gnarly_status_*  ; do
    display_name=$(basename "$display")
    if prompt_yn "Do you wish to install $display_name" ; then
      echo "nohup \"./$display_name\" >> \$GNARLY_LOG 2>&1 &" >> "$DISPLAY_SCRIPT"
    fi
  done
fi


