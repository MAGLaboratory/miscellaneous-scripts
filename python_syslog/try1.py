import logging
from logging.handlers import SysLogHandler
import sys

handler = SysLogHandler(
    facility=SysLogHandler.LOG_DAEMON,
    address="/dev/log"
    )
stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level = logging.DEBUG,
    handlers = [handler, stdout_handler]
    )
logging.debug("Sending a log message.")

