## System Configuration

In the root directory of the repo and on the system, there is a file called `gnarlypi.yml` this is a [YAML](https://en.wikipedia.org/wiki/YAML) file and contains some of the configuration for the system

In a YAML file lines that start with a '#' symbol are considered to be comments and are not processed.

In my version of the YAML file, it is possible to reference environment variables that have been setup before the reading program starts, these need to be wrapped in braces, e.g. in the command line environment `$HOME` would be the users home directory but in this configuration YAML file, it is referenced as `${HOME}`.
It is also possible to reference other entries in the file, using `dot notation`, these need to be in brackets, e.g. `$(gnarypi.logfile)`

A sample configuration file for the pitft display would be
```yaml
status:
  devices:
    # - gnarly_status_basic
    # - gnarly_status_blinkt
    # - gnarly_status_curses
    # - gnarly_status_ledshim
    - gnarly_status_pitft
    - gnarly_status_web
  pitft:
    rotation: 0
    font_size: 24
    display_height: 240
    display_width: 240
    x_offset: 0
    y_offset: 80
    newline: 28

gnarlypi:
  store: "${HOME}/usb_data/"
  force: false
  logfile: "/tmp/gnarlypi.log"
  loglevel: "debug"
  apps:
    - gnarly_indexer
    - gnarly_rsync

indexer:
  files: "$(gnarlypi.store)/files"
  index: "$(gnarlypi.store)/index"

status_web:
  port: 8027

rsync:
  source: "$(indexer.index)"
  target: ${USER}@homeassistant:/forSamba/NVME/Pictures
  sleep: 300
```

In this example, we can see that all of the status devices are commented out except for `gnarly_status_pitft`. Also we are using the `usb_data` directory which is a subdirectory of the users `${HOME}` directory. The indexer then uses the `store` base directory to setup two values and finally the `rsync` entry uses the value calculated in `indexer.index` to decide where to copy files from

### status section

**devices** this is an array of the device status programs to start when the main gnarlypi application starts, these can be found in the `status` directory, only start the ones that are relevant to the devices that you have connected to your rPI.

- `gnarly_status_pitft` - uses either the 135x240 or 240x240 Adafruit MiniTFT display (https://thepihut.com/products/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi-ada4393 or https://thepihut.com/products/adafruit-mini-pitft-1-3-240x240-tft-add-on-for-raspberry-pi)
- `gnarly_status_web` - runs a webserver that your computer browser can connect to
- `gnarly_status_ledshim` - uses the basic light bar https://thepihut.com/products/led-shim
- `gnarly_status_blinkt` - uses the extra basic light bar https://thepihut.com/products/blinkt
- `gnarly_status_curses` - should not be run via gnarlypi as it reports to the console
- `gnarly_status_basic` - should not be run via gnarlypi as it reports to the console 

**devices.pitft** this subsection is used by the mini_pitft (135x240) and the pitft devices (240x240)

- `rotation` is 90, 270 for the mini_pitft and, 0 or 180 for the pitft 
- `font_size` is the size of the font
- `newline` is the vertical line spacing, slightly more than the font size
- `display_height` and `display_width` set the size of the display
- `x_offset` and `y_offset` are used to show where the writable area starts

For the 135x240 display the section would be
```yaml
 # mini pitft config
  pitft:
    rotation: 270
    font_size: 14
    display_height: 135
    display_width: 240
    x_offset: 53
    y_offset: 40
    newline: 16
```
and for the 240x240 display the section is
```yaml
  # full size pitft
  pitft:
    rotation: 0
    font_size: 24
    display_height: 240
    display_width: 240
    x_offset: 0
    y_offset: 80
    newline: 28
```

### gnarlypi section

**store** this is where the gnarlypi application stores its files, there should be no need to change this from its default, unless you have added another storage device to your system - note that the storage device should be formatted as a ext2, ext3 or ext4 partition, otherwise the indexer will not be able to create symlinks.

**force** force overwriting of the image files, generally this should be **false**, so that when copying from your camera/SD card, only new files will be copied, otherwise all image files will be copied each time, which may take quite some time!

**logfile** where should any log file be written, if this is empty or the field does not exist, then there will not be a logfile created. If needed, write it to the `/tmp` directory, so that it will be wiped on system reboot, there is generally no need to maintain this and not writing it to your storage device would be advantageous.

**loglevel** what level of debug is needed, default to "debug", the usual levels can be used, "info", "warn", "error" etc.

**apps** - this is an array of the other gnarlypi applications that should be started up when the main gnarlypi application starts, these applications reside in the `bin` directory. Currently `gnarly_rsync` and `gnarly_indexer` are the only programs available

### indexer section

If the indexer application has been declared as one of the apps to run from the gnarlypi section, then it will read this section of the config.

**files** this is where the files are read from

**index** this is where symlinks to the original files will be created, symlinks are valid on linux drives (ext2, ext3 and ext4) and use very little space, these symlinks will be available either when connecting to the system over Samba or may be used when copying to a remote system, such as a NAS.

### rsync section

If the rsync application has been declared as one of the apps to run from the gnarlypi section, then it will read this section of the config.

**source** This is where the files will be read from and if using the indexer, this would be the place to read them from
The example reads the files linked in the index on a date basis, however, if you have a Sony camera or maybe a Panasonic and you require the full set of files in an expected order of folders, then change this to be `source: "$(indexer.files)"` so that the *DCIM* and *PRIVATE* folders will be copied over to your NAS.

**target** This is where files will be copied to, this could be a remote system that allows a SSH/SFTP or rsync connection as is shown in the example but could also be a local path that is a mount point for a remote system such as a NAS

**sleep** This is the time in seconds before rsync backup attempts. If the system is not connected to a network, then nothing happens with the rsync. If it is connected to a network, such as when you are at home, then its useful for this to be a shortish value such as **300** i.e. 5 minutes, so that your images will be backed up quite quickly after you have copied them from your SD card.

### status_web section

If using the web status reporter, it is possible to define the port that the web server is listening on

**port** This is the port number, in this config example we are using port 8027. You would connect to it from your browser as `http://devicename:8027/` replacing device name with either the name that your system knows the gnarlypi as or its IP address e.g. `http://192.168.0.128:8027/`

