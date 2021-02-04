import logging
import subprocess

from . import reformatter
from . import sync
from .dynamic import env_dict
from bot.helper.telegram_helper.message_utils import sendMessage

LOGGER = logging.getLogger(__name__)


def cfg_dat():
    dat = open('config.env', 'r+').read().replace(' = ', '\n').replace('"', '').split('\n')
    env_name = []
    env_value = []
    i = 1
    while i <= (dat.__len__() / 2):
        env_name.append(dat[(i - 1) * 2])
        env_value.append(dat[(i * 2) - 1])
        i += 1
    return env_name, env_value


def cfg_bak(update, context):
    cfg_bak_cmd = ['cp', '-v', 'config.env', 'config.env.bak']
    LOGGER.info(subprocess.run(cfg_bak_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    sendMessage("Copied 'config.env' to 'config.env.bak'", context.bot, update)


def handler(update, context):
    reformatter.handler()
    cfg_bak(update, context)
    env_name, env_value = cfg_dat()
    dat_new = ''
    i = 0
    while i <= (env_name.__len__() - 1):
        dat_new = dat_new + f'{env_name[i]} = {env_value[i]}' + '\n'
        i += 1
    sendMessage(dat_new, context.bot, update)
    file_name = 'config.env'
    result_str = sync.handler(file_name, env_dict[file_name.upper().replace('.', '_')])
    sendMessage(result_str, context.bot, update)
