 #!/usr/bin/env python3

from .messaging import Messaging

# ----------------------------------------------------------------------------


class Status:
    """Status
    class to handle sending status messages via MQTT to the correct message queue
    status = Status( 'servername')

    Args:
        server (str)            defaults to localhost

    """

    def __init__(self, server="localhost") -> None:
        self.server = server
        self.msg = Messaging()
        self.msg.connect(None, self.server)

    # ----------------------------------------------------------------------------
    def error(self, error_msg, error_lvl=0, msg2=""):
        """error - report an error
        Args:
            error_msg (str)     error message to be displayed
            error_lvl (int)     concern level of the error, the higher the error_lvl
                                the more concerning it is 1..3

            msg2      (str)     a secondary message that can be displayed on some
                                status devices
        """

        self.msg.publish(
            "/photos/error", {"msg": error_msg, "level": error_lvl, "msg2": msg2}
        )
        print(f"status.py Status error: {error_msg} level: {error_lvl} msg2: {msg2}")

    # ----------------------------------------------------------------------------
    def ready(self, msg):
        """show that the system is ready to accept an SD card insertion"""
        if not msg or msg is None:
            msg = "Insert SD Card"
        print( f"status.py Status ready: {msg}" )
        self.msg.publish("/photos/ready", {"msg": msg})

    # ----------------------------------------------------------------------------
    # this may be ignored by some devices
    def card_inserted(self):
        """show that an SD card has been inserted"""
        self.msg.publish("/photos/inserted")

    # ----------------------------------------------------------------------------
    def startcopy(self, file_count=0):
        """show that the overall copy process has started"""
        self.msg.publish("/photos/startcopy", {"files_total": file_count})

    # ----------------------------------------------------------------------------
    def endcopy(self, files_copied=0, file_count=0):
        """show that all the file copy operations have concluded

        Args:
            files_copied (int)      The number of files copied
            files_total  (int)      The total number of files on the device that
                                    could have been copied
        """
        self.msg.publish(
            "/photos/endcopy",
            {
                "files_copied": files_copied,
                "files_total": file_count,
            },
        )

    # ----------------------------------------------------------------------------
    # status device may choose to ignore this
    # info about individual file copy and the overall file copy data
    def copydata(
        self,
        fromfile,
        tofile,
        filesize=0,
        bytes_copied=0,
        files_copied=0,
        file_count=0,
        bps=0,
    ):
        """update data during a file copy process

        Args:
            fromfile        (str)   name of the file being copied
            tofile          (str)   name of the file at the destination
            filesize        (int)   size of the file to be copied
            bytes_copied    (int)   number of bytes copied so far
            files_copied    (int)   number of files copied so far
            file_count      (int)   total number of files to be copied
            bps             (int)   for secondary programs that perform copy processes,
                                    send the bytes per second
        """
        self.msg.publish(
            "/photos/copydata",
            {
                "fromfile": fromfile,
                "tofile": tofile,
                "size": filesize,
                "copied": bytes_copied,
                "files_copied": files_copied,
                "files_total": file_count,
                "bps": bps,
            },
        )

    # ----------------------------------------------------------------------------
    # waiting for the removal of the SD card
    def waitremove(self):
        """show that system is waiting for the removal of the SD card"""
        self.msg.publish("/photos/waitremove")

    # ----------------------------------------------------------------------------
    def diskfull(self, diskname):
        """show that the target disk is full

        Args:
            diskname (str)      name of the disk that is full, keep it short!
        """
        self.msg.publish("/photos/diskfull", {"diskname": diskname})

    # ----------------------------------------------------------------------------
    def devicedata(self, sd_size, sd_free, hd_size, hd_free):
        """send information about the source and target drives

        Args:
            sd_size (int)   overall size of the SD card in bytes
            sd_free (int)   number of bytes free on the SD card
            hd_size (int)   overall size of the target drive in bytes
            hd_free (int)   number of bytes free on the target drive
        """
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
        """send a keepalive message"""
        self.msg.publish("/photos/keepalive")

    # ----------------------------------------------------------------------------
    def fivelines(self, lines, color=None):
        """send five SHORT lines of information, target device may truncate

        Args:
            lines  (list of str)    array of 5 strings
            color  (str)
        """
        # slice to 5 lines
        self.msg.publish("/photos/fivelines", {"color": color, "lines": lines[:5]})

    # ----------------------------------------------------------------------------
    # allow the caller to clear the display, or the receivers appropriate part
    # of the display
    def clear(self):
        """clear/blank the display"""
        self.msg.publish("/photos/cls")

    # ----------------------------------------------------------------------------
    def buttonpress(self, button):
        """send a single button press

        Args:
            button (str)   single button character to send
        """
        # slice to a single character
        self.msg.publish("/photos/button", {"button": button[:1]})

    # ----------------------------------------------------------------------------
    def app_resume(self):
        """tell the main app, that a sub app has completed

        Args:
        """
        # slice to a single character
        self.msg.publish("/photos/app_resume", {})

    # ----------------------------------------------------------------------------
    def indexfile(self, filename):
        """create index symlinks for file in the destdir

        Args:
            filename (str)  full path to the file to be index
        """
        self.msg.publish("/photos/indexfile", {"filename": filename})

    # ----------------------------------------------------------------------------
    def indexdir(self):
        """re-create index symlinks, config file holds directory info,
        all previous index should be removed

        """
        self.msg.publish("/photos/indexdir")

    # ----------------------------------------------------------------------------
    def indextrip(self):
        """create trip index symlinks from files in index/date/{YYYY-MM-DD}"""
        self.msg.publish("/photos/indextrip")


    # ----------------------------------------------------------------------------
    def show_mode( self, data ):
        """send the mode to the display, while anything can be sent
        copy, index and sync are currently the usual ones, they should be True
        or False

        Args:
            data (dict)     mode data to be displayed
        """
        # print( f"show_mode {data}")
        self.msg.publish( "/photos/show_mode", data )
