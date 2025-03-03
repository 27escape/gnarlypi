#!/usr/bin/env python3

import fasteners

LOCKFILE = "/tmp/gnarlypi.lock"


class Lock:
    """class to provide locking for GnarlyPi apps,
    prevents main app from running when sub-apps want to do things

    Args:
        filename (str)  File to be used as the lockfile,
                        there is a default for gnarlypi

    """

    def __init__(self, lockfile=LOCKFILE) -> None:
        self.lockfile = lockfile
        self.lock = fasteners.InterProcessLock(self.lockfile)

    """wait for the gnarlypi lock file to be acquired"""
    def waitLock( self):
        print( "waitlock")
        self.lock.acquire()


    """release for the gnarlypi lock file"""
    def releaseLock( self):
        print( "releaselock")
        self.lock.release()
