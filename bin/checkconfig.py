#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, "../")
from libs.config import Config


# get config from default location $GNARLYPI_CONFIG
config = Config()

# ----------------------------------------------------------------------------

if __name__ == "__main__":


    print( "gnarlypi status: ", config.get("status"))
    print( "gnarlypi gnarlypi: ", config.get("gnarlypi"))
    print( "gnarlypi indexer: ", config.get("indexer"))
    print( "gnarlypi rsync: ", config.get("rsync"))
    print( "gnarlypi hotspot", config.get("hotspot"))
    print( "gnarlypi wifi", config.get("wifi"))