import logging
import re
import subprocess

from bot.helper.telegram_helper.message_utils import sendMessage

LOGGER = logging.getLogger(__name__)


def helper(update, context):
    uncommented = ''
    for line in open('config.env', 'r+').readlines():
        commented = re.findall("^#", line)
        newline = re.findall("^\n", line)
        if not commented and not newline:
            uncommented = uncommented + line

    open('config.env', 'w').write(uncommented)
    cfg_bak_cmd = ['cp', '-v', 'config.env', 'config.env.bak']
    subprocess.run(cfg_bak_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    sendMessage("Copied 'config.env' to 'config.env.bak'", context.bot, update)
    config_env = open('config.env', 'r+')
    cfg_dat = config_env.read().replace(' = ', '\n').split('\n')
    config_env.close()
    i = 1
    # str = ''
    while i <= ((cfg_dat.__len__()) - 1) / 2:
        # str = str + f'(LINE-{i})\n{cfg_dat[(i-1)*2]} = {cfg_dat[(i*2)-1]}\n'
        sendMessage(f'(LINE-{i})\n{cfg_dat[(i - 1) * 2]} = {cfg_dat[(i * 2) - 1]}', context.bot, update)
        i += 1
    # sendMessage(str, context.bot, update)
