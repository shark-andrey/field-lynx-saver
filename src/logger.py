import sys

from loguru import logger


logger.remove()
logger.add(
    sys.stdout,
    format="[{time:YYYY-MM-DD HH:mm:ss}] <lvl>{message}</lvl>",
    level="DEBUG",
    colorize=True,
    backtrace=True,
)
