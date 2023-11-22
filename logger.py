""" loguru
TRACE       5   logger.trace()
DEBUG       10  logger.debug()
INFO        20  logger.info()
SUCCESS     25  logger.success()
WARNING     30  logger.warning()
ERROR       40  logger.error()
CRITICAL    50      logger.critical()

COLORS ["blue", "cyan", "green", "magenta", "red", "yellow"]
"""

import os
import sys
import time
import threading

from typing import Callable

from loguru import logger


class Logger:
    def __init__(self, level: str = "INFO", log_path: str = "log", log_name: str = "log.log"):
        self._local = threading.local()
        self._local.buffer = ""
        self._log_name = os.path.join(log_path, log_name)
        self._set_logger(level, self._log_name)

    @classmethod
    def _set_logger(cls, level: str = "INFO", log_path: str = "log/log.log"):
        # Remove all handlers added so far
        logger.remove()

        # custom level
        logger.level("NOTICE", no=25, color="<blue><bold>")
        logger.level("WARN", no=30, color="<yellow><bold>")
        logger.level("FATAL", no=50, color="<magenta><bold>")

        # formatter
        fmt = "[<level>{level: <6}</level>]" \
              "[<green>{time:YYYY:MM:DD HH:mm:ss}</green>]" \
              "[<yellow>pid</yellow>:{process.id}]" \
              "[<yellow>tid</yellow>:{thread.id}]" \
              "[<cyan>{file.name}</cyan>:{line}]" \
              "{message}"

        # to console
        logger.add(sink=sys.stdout,
                   format=fmt,
                   level=level,
                   serialize=False)

        # to file
        # rotation: Automatically rotate too big file, 200 KB, 100 MB
        # retention: Cleanup after some time or some files
        logger.add(sink=log_path,
                   filter=lambda record: "download" not in record["extra"],
                   format=fmt,
                   rotation="100 MB",
                   retention=10,
                   enqueue=True,
                   serialize=False)

        logger.add(sink="./log/download.log",
                   filter=lambda record: "download" in record["extra"],
                   format=fmt,
                   rotation="100 MB",
                   retention=10,
                   enqueue=True,
                   serialize=False
                   )

    def add_notice(self, key, value):
        if not hasattr(self._local, "buffer"):
            self._local.buffer = ""
        self._local.buffer += "[{}:{}]".format(key, value)

    def debug(self, fmt, *args):
        logger.opt(depth=2).debug(fmt, *args)

    def notice(self, fmt, *args):
        logger.opt(depth=2).info(fmt, *args)

    def warn(self, fmt, *args):
        logger.opt(depth=2).log("WARN", fmt, *args)

    def error(self, fmt, *args):
        logger.opt(depth=2).error(fmt, *args)

    def fatal(self, fmt, *args):
        logger.opt(depth=2).log("FATAL", fmt, *args)

    def flush(self):
        if not hasattr(self._local, "buffer"):
            self._local.buffer = ""
        logger.opt(depth=2).log("NOTICE", self._local.buffer.rstrip())
        self._local.buffer = ""

    def bind(self, key, *args):
        logger.bind(download=key).info("request_id:{}|cost:{}".format(args[1],args[0]))

_aip_logger = Logger()
_time_cost_dict = {}


def tic(name="cost"):
    _time_cost_dict["{}_{}".format(threading.get_ident(), name)] = time.time()


def toc(name="cost"):
    cost = time.time() - _time_cost_dict["{}_{}".format(threading.get_ident(), name)]
    add_notice(name, "{:.2f}ms".format(cost * 1000))
    return cost


def add_notice(key, value):
    _aip_logger.add_notice(key, value)


def debug(fmt, *args):
    _aip_logger.debug(fmt, *args)


def notice(fmt, *args):
    _aip_logger.notice(fmt, *args)


def warn(fmt, *args):
    _aip_logger.warn(fmt, *args)


def swarn(seconds, fmt, *args):
    time.sleep(seconds)
    _aip_logger.warn(fmt, *args)


def error(fmt, *args):
    _aip_logger.error(fmt, *args)


def fatal(fmt, *args):
    _aip_logger.fatal(fmt, *args)


def flush():
    _aip_logger.flush()


def bind(key="download", *args):
    _aip_logger.bind(key, *args)

def timeit(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        tic(func.__name__)
        res = func(*args, **kwargs)
        toc(func.__name__)
        return res

    return wrapper
