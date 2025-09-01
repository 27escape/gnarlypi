# consistent logging setup for the applications

import os
import logging
import inspect
from logging.handlers import TimedRotatingFileHandler


class DebugLogger:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(caller_file)s:%(caller_line)d %(message)s'
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def _log(self, level, msg, *args, **kwargs):
        # Get caller's frame
        frame = inspect.currentframe().f_back.f_back
        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        extra = {'caller_file': filename, 'caller_line': lineno}
        self.logger.log(level, msg, *args, extra=extra, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)



def Debug(name, logfile=None, level=logging.INFO):
    """Initialize logging for the application."""

    logger = logging.getLogger(name=__file__)      
    # debugger = DebugLogger( logger)     
      
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
        # debugger.info("Started")
    else:
        if loglevel != logging.NOTSET:
            logging.basicConfig(
                level=loglevel,
                format="%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        print("no logfile set")
        
    return logger
    