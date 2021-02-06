import shutil
import psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from . import dispatcher, updater, botStartTime
from .helper.ext_utils import fs_utils
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .helper.config import editor
from .helper.config import sync
from .helper.config.dynamic import fileIdDict
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Bot Uptime:</b> {currentTime}\n' \
            f'<b>Total disk space:</b> {total}\n' \
            f'<b>Used:</b> {used}  ' \
            f'<b>Free:</b> {free}\n\n' \
            f'📊Data Usage📊\n<b>Upload:</b> {sent}\n' \
            f'<b>Down:</b> {recv}\n\n' \
            f'<b>CPU:</b> {cpuUsage}% ' \
            f'<b>RAM:</b> {memory}% ' \
            f'<b>Disk:</b> {disk}%'
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    start_string = f'''
A Bot to mirror files on the internet to Google Drive.
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
    sendMessage(start_string, context.bot, update)


@run_async
def restart(update, context):
    file_name = 'token.pickle'
    file_id = fileIdDict[file_name.upper().replace('.', '_')]
    sync.handler(file_name, file_id, usePatch=False, update=update, context=context)
    restart_message = sendMessage("Restarting, Please Wait!", context.bot, update)
    LOGGER.info(f'Restarting the Bot...')
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def config(update, context):
    editor.handler(update, context)


@run_async
def bot_help(update, context):
    help_string = f'''
/{BotCommands.StartCommand} Start the bot

/{BotCommands.MirrorCommand} Mirror the provided link to Google Drive

/{BotCommands.UnzipMirrorCommand} Mirror the provided link and if the file is in archive format, it is extracted and then uploaded to Google Drive

/{BotCommands.TarMirrorCommand} Mirror the provided link and upload in archive format (.tar) to Google Drive

/{BotCommands.CancelMirrorCommand} Reply with this command to the source message, and the download will be cancelled

/{BotCommands.CancelAllCommand} Cancels all running tasks (downloads, uploads, archiving, unarchiving)

/{BotCommands.ListCommand} Searches the Google Drive folder for any matches with the search term and presents the search results in a Telegraph page

/{BotCommands.StatusCommand} Shows the status of all downloads and uploads in progress

/{BotCommands.AuthorizeCommand} Authorize a group chat or, a specific user to use the bot

/{BotCommands.UnAuthorizeCommand} Unauthorize a group chat or, a specific user to use the bot

/{BotCommands.PingCommand} Ping the bot

/{BotCommands.RestartCommand} Restart the bot

/{BotCommands.StatsCommand} Shows the stats of the machine that the bot is hosted on

/{BotCommands.HelpCommand}: To get the help message

/{BotCommands.LogCommand} Sends the log file of the bot (can be used to analyse crash reports, if any)

/{BotCommands.CloneCommand} Clone folders in Google Drive (owned by someone else) to your Google Drive

/{BotCommands.WatchCommand} Mirror through 'youtube-dl' to Google Drive

/{BotCommands.TarWatchCommand} Mirror through 'youtube-dl' and upload in archive format (.tar) to Google Drive

/{BotCommands.DeleteCommand} Delete files in Google Drive matching the given string

/{BotCommands.ConfigCommand} Edit 'config.env' file

'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        LOGGER.info('Restarted Successfully!')
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart, filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    config_handler = CommandHandler(BotCommands.ConfigCommand, config, filters=CustomFilters.owner_filter)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(config_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
