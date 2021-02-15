import threading
from telegram.ext import CommandHandler, run_async
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher, USE_TELEGRAPH
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands


@run_async
def list_drive(update, context):
    if USE_TELEGRAPH:
        try:
            search = update.message.text.split(' ', maxsplit=1)[1]
            LOGGER.info(f"Searching: {search}")
            reply = sendMessage('Searching..... Please Wait!', context.bot, update)
            gdrive = GoogleDriveHelper(None)
            msg, button = gdrive.drive_list(search)
            if button:
                editMessage(msg, reply, button)
            else:
                editMessage('No results found', reply, button)
        except IndexError:
            sendMessage('Send a search key along with command', context.bot, update)
    if not USE_TELEGRAPH:
        message = update.message.text
        search = message.split(' ', maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}...")
        gdrive = GoogleDriveHelper(None)
        msg = gdrive.drive_list(search)
        if msg:
            reply_message = sendMessage(msg, context.bot, update)
        else:
            reply_message = sendMessage('No results found', context.bot, update)
        threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(list_handler)
