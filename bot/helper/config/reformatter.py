import logging
import re

LOGGER = logging.getLogger(__name__)


def handler():
    formatted = ''
    for line in open('config.env', 'r+').readlines():
        commented = re.findall("^#", line)
        newline = re.findall("^\n", line)
        if not commented and not newline:
            formatted = formatted + line
    open('config.env', 'w').write(formatted)
    LOGGER.info("Reformatted 'config.env'")
