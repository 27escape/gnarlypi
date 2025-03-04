# Improvements / TODO

Interaction:
- allow limited button presses, only when not copying from SD, can still use some of the '/photo' topics to give status of actions
  - maybe 2 buttons as default, to give 3 interactions: A (as Yes), B (as No) and A+B (as C/Cancel/Back)
  - [-] delete files from USB? Only allow if ONE connected device, to ensure correct choice - difficult for cameras with multiple card slots - user needs to remove each card, needs confirmation step
    - **decision**: do not implement, leave SD card/camera storage manage to user
  - [ ] delete files from storage? could be done via Samba, could be done via web
  - [x] rsync to NAS/computer - target defined in some config file, check target available before attempt 

During copy process:
- extract image thumbnails for 
- [ ] Create day/trip indexes to each file that can be accessed via Samba/smb shares
  - Create folder for each day/trip with symlinks to the relevant images
  - a complete re-index script, inc thumbnail extraction


Management: 
- [ ] Create web app for management
  - [ ] view/delete images or block wipe
  - [ ] gnarlypi.yaml config management
  - [ ] investigate photo album software
- [ ] investigate creating WiFi hotspot network, when away from home
- initial startup QR code for access to initial hotspot to config system
  - also default hotspot so devices that do not have big displays can still be configured




Getting files off device:
- [ ] investigate USB Gadget mode for Pi Zero 2
  - allows personal devices to connect to samba/photo album for edit/sharing images

Device improvements:
- [ ] power button for non PI 5 devices?
  - For devices that do not provide an off switch (nice shutdown), we will need to investigate options to replicate that, either with buttons provided by any display choice or by adding our own switch, this is especially important for the PI's without a power button, check out https://howchoo.com/pi/how-to-add-a-power-button-to-your-raspberry-pi/ for a solution to that issue 
  - the [OnOff SHIM](https://thepihut.com/products/onoff-shim) _may_ be a solution but button placement is not ideal, a secondary button will need soldering, intial trials show it may conflict with the adafruit PiTFT displays

- [ ] CFexpress? My cameras don't use these cards, so this would only be added if anyone else needs it, ideally its just another USB device and should read and copy fine, without any code changes


## Investigate all in one solutions:

The idea is that there may be something that is not specifically created to be a camera backup device but could be repurposed into being one. If you want something pre-made, checkout some [alternatives](./alternatives.md)

There are interesting things over at [ClockworkPi](https://www.clockworkpi.com/shop) that seem to be based on the CM4 compute modules, which would mean external USB for storage, but that could be fine and things do not have to be super fast :)

Would the [Zero Terminal](https://n-o-d-e.net/zeroterminal3.html) be a nice all in one device? _It does not look like this has had development in years and I cannot figure out how to contact the developer_

For the PI 5, the [KKSB 7" display case](https://thepihut.com/products/kksb-case-for-raspberry-pi-5-and-the-official-raspberry-pi-7-touchscreen) could be a nice but I would need to create the web app to provide display and control features.

Little Bird Electronics used to have a nice [PI 3 display/keyboard combo](https://littlebirdelectronics.com.au/products/raspberry-pi-3-2b-zero-mini-portable-2-4ghz-wireless-touchpad-keyboard-with-backlight) _but it is no longer available_

Something like the [Micro Journal rev 2](https://liliputing.com/micro-journal-rev-2-revamp-is-a-compact-word-processor-with-a-mechanical-keyboard-and-a-clamshell-design/) could work _but needs storage and SD card capabilities_

[Planet Computers](https://www.www3.planetcom.co.uk/) may have a suitable device but would need to a USB hub to have bigger external storage. The Gemini and Cosmo models are kinda at the top end of the price range for what I am trying to achieve. _Not sure if they are still in operation_

For something that is not rPi based, then the linux based https://www.unihiker.com/, its around $80, so may be interesting, not as powerful but built in screen and memory, would still need to add an SD card reader, maybe something nice could be done with a 3D printer here
