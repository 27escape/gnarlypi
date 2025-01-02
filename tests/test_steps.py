#!/usr/bin/env python3

import time
import sys
sys.path.insert( 0, '../')
from libs.status import Status  # type: ignore

# ----------------------------------------------------------------------------



def progressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = "0"
    try:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
    except:
        percent = "0"
        filledLength = 0
    bar = fill * filledLength + ' ' * (length - filledLength)
    return f'{prefix} [{bar}] {percent}% {suffix}'


print( ProgressBar( 2, 100, 'a', 'b', 0, 50))




# print( 'sending MQTT status messages')
# status = Status()

# status.error("cannot do something", 3)
# time.sleep(1)
# status.ready()
# time.sleep(1)
# status.devicedata(65536, 40000, 2097152, 195715)
# time.sleep(1)
# status.startcopy()
# time.sleep(0.1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/thefile.jpg",
#     "/home/kevinmu/usb_data/101/thefile.jpg",
#     10100,
#     2000,
#     25,
#     100
# )
# time.sleep(1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/thefile.jpg",
#     "/home/kevinmu/usb_data/101/thefile.jpg",
#     10100,
#     4000,
#     25,
#     100,
# )
# time.sleep(1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/thefile.jpg",
#     "/home/kevinmu/usb_data/101/thefile.jpg",
#     10100,
#     6000,
#     25,
#     100,
# )
# time.sleep(1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/thefile.jpg",
#     "/home/kevinmu/usb_data/101/thefile.jpg",
#     10100,
#     8000,
#     25,
#     100,
# )
# time.sleep(1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/thefile.jpg",
#     "/home/kevinmu/usb_data/101/thefile.jpg",
#     10100,
#     10100,
#     75,
#     100,
# )
# time.sleep(1)
# status.copydata(
#     "/mnt/sdcard/DCIM/101/newfile.jpg",
#     "/home/kevinmu/usb_data/101/newfile.jpg",
#     10100,
#     10100,
#     76,
#     100,
# )
# status.copydata(
#     "/mnt/sdcard/DCIM/101/newfile2.jpg",
#     "/home/kevinmu/usb_data/101/newfile2.jpg",
#     10100,
#     10100,
#     77,
#     100,
# )
# time.sleep(1)
# status.endcopy()
# time.sleep(1)
# status.devicedata(65536, 40000, 2097152, 289715)
# time.sleep(1)
# status.waitremove()
# time.sleep(1)
# status.diskfull("/mnt/some_usb")
