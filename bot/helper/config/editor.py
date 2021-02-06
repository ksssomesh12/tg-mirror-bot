import logging
import subprocess

from . import reformatter
from . import sync
from .dynamic import fileIdDict
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.bot_commands import BotCommands

LOGGER = logging.getLogger(__name__)


def cfg_bak(update, context):
    cfg_bak_cmd = ['cp', '-v', 'config.env', 'config.env.bak']
    LOGGER.info(subprocess.run(cfg_bak_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    sendMessage("Copied 'config.env' to 'config.env.bak'", context.bot, update)


def handler(update, context):
    reformatter.handler('config.env')
    # cfg_bak(update, context)
    file_name = 'config.env'
    file_id = fileIdDict[file_name.upper().replace('.', '_')]
    sync.handler(file_name, file_id, usePatch=False, update=update, context=context)
    req_restart_msg = f"Please /{BotCommands.RestartCommand} to load changes made to 'config.env'"
    LOGGER.info(req_restart_msg)
    sendMessage(req_restart_msg, context.bot, update)
