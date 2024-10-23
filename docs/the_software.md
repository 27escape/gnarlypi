# The code itself

The main code that controls things is written in Python, mostly because the majority of the devices you can buy and attach to your Raspberry Pi have Python libraries and I did not want to start from scratch. Also it was an opportunity to write some python and hopefully improve things.

I decided from the start to use a messaging system for the displays, this way I would not need to constantly fiddle with the main code, inserting ifs and buts for another display. Adding a new display mechanism is straight forwards and separate to the main code and can be tested  

## The software so far

- **be_gnarly** - this is called from cron and starts up all the required scripts to run the system
- **display_config.sh** - choose which of the display options you wish to use
- **gnarly_status_basic** - mostly for testing, displays MQTT messages in the terminal
- **gnarly_status_blinkt** - simple LED only status display 
- **gnarly_status_curses** - more advanced terminal display, needs work to tidy it up and stop screen flashes/tearing
- **gnarly_status_ledshim** - a longer simple LED only status display
- **gnarly_status_mini_pitft** - a compact 5 line 135x240 pixel display HAT, currently the nicest way to display status 
- **gnarly_status_pitft** - big sister to the mini above, a 240x240 pixel display HAT, currently the nicest way to display status - RECOMMENDED!
- **gnarlypi** - the main code, this does the copying
- **installer.sh** - the installer!
- _start_displays.sh_ - this script will be created by `display_config.sh` 
- **display_config.sh** - script to chose output displays, run as part of installer, creates _start_displays.sh_
- _tests/test_mini_pitft.py_**_ - test the the mini_pitft is working
- _test_status.py_ - test status displays by single step through a selection of MQTT messages

For extra testing, it is possible, by using [mqtt2jsonl](https://github.com/27escape/mqtt2jsonl), to record and replay the MQTT messages, in real-time, to simulate a complete copy of files from a USB to the storage device - very handy!
