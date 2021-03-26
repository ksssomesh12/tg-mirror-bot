from telegram.ext import CommandHandler
from tgmb.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from tgmb import LOGGER, dispatcher
from tgmb.helper.telegram_helper.message_utils import sendMessage, editMessage
from tgmb.helper.telegram_helper.filters import CustomFilters
from tgmb.helper.telegram_helper.bot_commands import BotCommands


def list_drive(update, context):
    if update.message.text == f'/{BotCommands.ListCommand}':
        sendMessage(f'Send a search key along with {BotCommands.ListCommand} command', context.bot, update)
    else:
        search = update.message.text.split(' ', maxsplit=1)[1]
        LOGGER.info(f"Searching: '{search}'...")
        reply = sendMessage('Searching.....\nPlease Wait!', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)
        if msg:
            if button:
                editMessage(msg, reply, button)
            else:
                editMessage(msg, reply)
        else:
            editMessage('No results found', reply)
        # if not USE_TELEGRAPH:
        #     threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply)).start()


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,
                              filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
