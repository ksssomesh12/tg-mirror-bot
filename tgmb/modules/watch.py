from telegram.ext import CommandHandler, run_async
from telegram import Bot, Update
from tgmb import Interval, DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL, dispatcher, LOGGER
from tgmb.helper.ext_utils.bot_utils import setInterval
from tgmb.helper.telegram_helper.message_utils import update_all_messages, sendMessage, sendStatusMessage
from .mirror import MirrorListener
from tgmb.helper.mirror_utils.download_utils.youtube_dl_download_helper import YoutubeDLHelper
from tgmb.helper.telegram_helper.bot_commands import BotCommands
from tgmb.helper.telegram_helper.filters import CustomFilters
import threading


def _watch(bot: Bot, update: Update, args: list, isTar=False):
    try:
        link = args[0]
    except IndexError:
        msg = f"/{BotCommands.WatchCommand} [yt_dl supported link] [quality] to mirror with youtube_dl.\n\n"
        msg += "Example of quality :- audio, 144, 360, 720, 1080.\nNote :- Quality is optional"
        sendMessage(msg, bot, update)
        return
    try:
        qual = args[1]
        if qual != "audio":
            qual = f'bestvideo[height<={qual}]+bestaudio/best[height<={qual}]'
    except IndexError:
        qual = "bestvideo+bestaudio/best"
    reply_to = update.message.reply_to_message
    if reply_to is not None:
        tag = reply_to.from_user.username
    else:
        tag = None

    listener = MirrorListener(bot, update, isTar, tag)
    ydl = YoutubeDLHelper(listener)
    threading.Thread(target=ydl.add_download, args=(link, f'{DOWNLOAD_DIR}{listener.uid}', qual)).start()
    sendStatusMessage(update, bot)
    if len(Interval) == 0:
        Interval.append(setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))


@run_async
def watchTar(update, context):
    _watch(context.bot, update, context.args, True)


def watch(update, context):
    _watch(context.bot, update, context.args)


mirror_handler = CommandHandler(BotCommands.WatchCommand, watch,
                                pass_args=True,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
tar_mirror_handler = CommandHandler(BotCommands.TarWatchCommand, watchTar,
                                    pass_args=True,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(mirror_handler)
dispatcher.add_handler(tar_mirror_handler)
