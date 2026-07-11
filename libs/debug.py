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



def setLogFile(logfile, name=None):
    """Point logging at the given file, replacing any handlers already set
    up (e.g. by Debug()'s default stdout StreamHandler), so output only goes
    to the new file rather than continuing to also go to the old destination.

    Uses the same rotate-nightly-keep-5-backups policy and message format as
    Debug(). Call this any time after Debug() to redirect logging - handy for
    switching a console-based tool from printing to stdout to writing to a
    file instead (e.g. when stdout is unusable, such as under curses).
    Creates the log file's parent directory if it doesn't already exist.
    If 2 processes logging to the same file name, at midnight, there is a 
    chance of one writing to 'yesterday' and the other writing to 'today'

    @params:
        logfile - Required : path to the log file to write to (Str)
        name    - Optional : logger name to configure; defaults to the root
                  logger, which is what Debug()'s basicConfig-based setup
                  attaches to (Str or None)
    """
    target_logger = logging.getLogger(name) if name else logging.getLogger()

    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # TimedRotatingFileHandler (like FileHandler) won't create missing
    # parent directories itself - it just raises FileNotFoundError - so do
    # that first
    log_dir = os.path.dirname(logfile)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # remove existing handlers first, so we don't end up logging to both the
    # old destination (e.g. stdout) and the new file at the same time
    for old_handler in list(target_logger.handlers):
        target_logger.removeHandler(old_handler)
        old_handler.close()

    handler = TimedRotatingFileHandler(
        logfile, when="midnight", interval=1, backupCount=5
    )
    handler.setFormatter(formatter)
    target_logger.addHandler(handler)

    return logfile


def Debug(name, logfile=None, level="INFO"):
    """Initialize logging for the application."""

    # logger = logging.getLogger(name=__file__)      
    logger = logging.getLogger(name=name)      
    # debugger = DebugLogger( logger)     
      
    match level.lower():
        case "debug" | logging.DEBUG:
            loglevel = logging.DEBUG
        case "info" | logging.INFO:
            loglevel = logging.INFO
        case "warning" | "warn" | logging.WARNING:
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