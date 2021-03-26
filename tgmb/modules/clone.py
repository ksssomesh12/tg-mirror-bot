from telegram.ext import CommandHandler
from tgmb.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from tgmb.helper.telegram_helper.message_utils import *
from tgmb.helper.telegram_helper.filters import CustomFilters
from tgmb.helper.telegram_helper.bot_commands import BotCommands
from tgmb import dispatcher


def cloneNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"Cloning: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result, button = gd.clone(link)
        deleteMessage(context.bot, msg)
        if button == "":
            sendMessage(result, context.bot, update)
        else:
            sendMarkup(result, context.bot, update, button)
    else:
        sendMessage("Provide G-Drive Shareable Link to Clone.", context.bot, update)


clone_handler = CommandHandler(BotCommands.CloneCommand, cloneNode,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(clone_handler)
