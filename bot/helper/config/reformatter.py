import logging
import re

LOGGER = logging.getLogger(__name__)


def handler(fileName: str):
    formatted = ''
    for line in open(fileName, 'r').readlines():
        commented = re.findall("^#", line)
        newline = re.findall("^\n", line)
        if not commented and not newline:
            formatted = formatted + line
    if open(fileName, 'r').read() == formatted:
        pass
    else:
        open(fileName, 'w').write(formatted)
        LOGGER.info(f"Reformatted '{fileName}'")
    return
