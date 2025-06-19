# consistent logging setup for the applications

import logging
from logging.handlers import TimedRotatingFileHandler


def Debug(name, logfile=None, level=logging.INFO):
    """Initialize logging for the application."""

    logger = logging.getLogger(name=__file__)      
      
    match level.lower():
        case "debug" | logging.DEBUG:
            loglevel = logging.DEBUG
        case "info" | logging.INFO:
            loglevel = logging.INFO
        case "warning" | logging.WARNING:
            loglevel = logging.WARNING
        case "error" | logging.ERROR:
            loglevel = logging.ERROR
        case "critical" | logging.CRITICAL:
            loglevel = logging.CRITICAL
        case "none" | "notset":
            loglevel = logging.NOTSET
        case _:
            loglevel = logging.NOTSET

    if logfile: 
            # filename=logfile,
            # "filemode": "a",
        logging_params = {
            "encoding": "utf-8",
            "format": "%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "level": loglevel,
            # Set up a rotating file handler for logging
            # rotates daily, keeping a maximum of 7 backups
            "handlers": [TimedRotatingFileHandler(logfile, when='midnight', interval=1, backupCount=5)]            
        }
              
        logging.basicConfig( **logging_params)
        logger.info("Started")
    else:
        if loglevel != logging.NOTSET:
            logging.basicConfig(
                level=loglevel,
                format="%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        print("no logfile set")
        
    return logger
    