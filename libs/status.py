#!/usr/bin/env python3

import signal
from .messaging import Messaging

# ----------------------------------------------------------------------------

# a private class that cannot be seen outside of this module

class Status:

    def __init__(self, server="localhost") -> None:
        self.server = server
        self.msg = Messaging()
        self.msg.connect( None, self.server)


    # ----------------------------------------------------------------------------
    def error(self, error_msg, error_lvl=0, msg2=""):
        """error - report an error, the higher the error_lvl the more concerning it is 1..3"""
        self.msg.publish("/photos/error", {"msg": error_msg, "level": error_lvl, "msg2": msg2})


    # ----------------------------------------------------------------------------
    def ready(self):
        """ready - show that the system is ready to accept an SD card insertion"""
        self.msg.publish("/photos/ready")


    # ----------------------------------------------------------------------------
    # this may be ignored by some devices
    def card_inserted(self):
        """card_inserted - show that an SD card has been inserted"""
        self.msg.publish("/photos/inserted")


    # ----------------------------------------------------------------------------
    # the overall copy process has started
    def startcopy(self, file_count=0):
        """ """
        self.msg.publish("/photos/startcopy", { "files_total": file_count})


    # ----------------------------------------------------------------------------
    # The overall copy process has completed
    def endcopy(self, files_copied=0, file_count=0):
        """ """
        self.msg.publish("/photos/endcopy",
            {
                "files_copied": files_copied,
                "files_total": file_count,
            },
        )


    # ----------------------------------------------------------------------------
    # status device may choose to ignore this
    # info about individual file copy and the overall file copy data
    def copydata(self,fromfile, tofile, filesize=0, bytes_copied=0, files_copied=0, file_count=0):
        """ """
        self.msg.publish(
            "/photos/copydata",
            {
                "fromfile": fromfile,
                "tofile": tofile,
                "size": filesize,
                "copied": bytes_copied,
                "files_copied": files_copied,
                "files_total": file_count,
            },
        )


    # ----------------------------------------------------------------------------
    # waiting for the removal of the SD card
    def waitremove(self):
        """ """
        self.msg.publish("/photos/waitremove")


    # ----------------------------------------------------------------------------
    # waiting for the removal of the SD card
    def diskfull(self, diskname):
        """ """
        self.msg.publish("/photos/diskfull", {"diskname": diskname})


    # ----------------------------------------------------------------------------
    # size of SD card, size of target disk, space remaining on each
    #  device status can chose to ignore this
    # sizes in bytes
    # this function may determine this data itself, based on drive mount point
    def devicedata(self, sd_size, sd_free, hd_size, hd_free):
        """ """
        self.msg.publish(
            "/photos/devicedata",
            {
                "sd_size": sd_size,
                "sd_free": sd_free,
                "hd_size": hd_size,
                "hd_free": hd_free,
            },
        )


    # ----------------------------------------------------------------------------
    # send this periodically to allow the display clients to know that the system is
    # still working
    def keepalive(self):
        """ """
        self.msg.publish("/photos/keepalive")

    # ----------------------------------------------------------------------------
    # send 5 short lines, eg for boot up msg
    def fivelines(self, lines, color=None):
        """ """
        # slice to 5 lines
        self.msg.publish("/photos/fivelines", {"color": color, "lines":lines[:5]})


    # ----------------------------------------------------------------------------
    # allow the caller to clear the display, or the receivers appropriate part
    # of the display
    def clear(self):
        """ """
        self.msg.publish("/photos/cls")


# instantiate the private class into variable that can be imported into other namespaces, it will act as a
# singleton to do all the status activities
# status = __Status__()
# status.connect()
