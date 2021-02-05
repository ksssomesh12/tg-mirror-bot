import logging
import subprocess

from . import reformatter
from . import sync
from .dynamic import fileIdDict
from bot.helper.telegram_helper.message_utils import sendMessage

LOGGER = logging.getLogger(__name__)


def cfg_bak(update, context):
    cfg_bak_cmd = ['cp', '-v', 'config.env', 'config.env.bak']
    LOGGER.info(subprocess.run(cfg_bak_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    sendMessage("Copied 'config.env' to 'config.env.bak'", context.bot, update)


def handler(update, context):
    reformatter.handler('config.env')
    cfg_bak(update, context)
    file_name = 'config.env'
    result_str = sync.handler(file_name, fileIdDict[file_name.upper().replace('.', '_')], usePatch=False)
    sendMessage(result_str, context.bot, update)
