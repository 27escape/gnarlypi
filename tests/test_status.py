#!/usr/bin/env python3

import time
import sys
sys.path.insert( 0, '../')
from libs.status import Status  # type: ignore

BLOCK_SIZE = 1024 * 1024 * 1024


def delay_action( txt, delay=1):
    print( txt)
    if delay == 1:
        input( 'press enter key')
    else:
        time.sleep( delay)

# ----------------------------------------------------------------------------

print( f"sending MQTT status messages\n")

status = Status()
delay_action( "status.error")
status.error("cannot do something", 3, "second error")

delay_action( "status.ready")
status.ready()

delay_action( "status.devicedata")
status.devicedata(65 * BLOCK_SIZE, 40* BLOCK_SIZE, 256 * BLOCK_SIZE, 80 * BLOCK_SIZE)

delay_action( "status.startcopy")
status.startcopy()

delay_action( "status.copydata 1/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/thefile.jpg",
    "/home/kevinmu/usb_data/101/thefile.jpg",
    10100,
    2000,
    25,
    100
)
delay_action( "status.copydata 2/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/thefile.jpg",
    "/home/kevinmu/usb_data/101/thefile.jpg",
    10100,
    4000,
    25,
    100,
)
delay_action( "status.copydata 3/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/thefile.jpg",
    "/home/kevinmu/usb_data/101/thefile.jpg",
    10100,
    6000,
    25,
    100,
)
delay_action( "status.copydata 4/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/thefile.jpg",
    "/home/kevinmu/usb_data/101/thefile.jpg",
    10100,
    8000,
    25,
    100,
)
delay_action( "status.copydata 5/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/thefile.jpg",
    "/home/kevinmu/usb_data/101/thefile.jpg",
    10100,
    10100,
    75,
    100,
)
delay_action( "status.copydata 6/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/newfile.jpg",
    "/home/kevinmu/usb_data/101/newfile.jpg",
    10100,
    10100,
    76,
    100,
)
delay_action( "status.copydata 7/6")
status.copydata(
    "/mnt/sdcard/DCIM/101/newfile2.jpg",
    "/home/kevinmu/usb_data/101/newfile2.jpg",
    10100,
    10100,
    77,
    100,
)

delay_action( "status.endcopy")
status.endcopy()

delay_action( "status.devicedata")
status.devicedata(65 * BLOCK_SIZE, 30* BLOCK_SIZE, 256 * BLOCK_SIZE, 70 * BLOCK_SIZE)

delay_action( "status.waitremove")
status.waitremove()

delay_action( "status.diskful")
status.diskfull("/mnt/some_usb")

print( "done")
