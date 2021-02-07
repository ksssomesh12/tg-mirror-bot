import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ConversationHandler, CallbackContext, CallbackQueryHandler
from . import reformatter
from . import sync
from .load import load_dat
from .dynamic import fileIdDict
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters


class InlineKeyboardMaker:
    def __init__(self, button_list: list):
        self.button_list = button_list
        self.buttons = []
        self.menu = []
        self.keyboard = []

    def build(self, cols: int):
        for i in range(0, len(self.button_list), 1):
            self.buttons.append(InlineKeyboardButton(text=self.button_list[i], callback_data=(i + 1)))
        self.menu = [self.buttons[i:i + cols] for i in range(0, len(self.buttons), cols)]
        self.keyboard = InlineKeyboardMarkup(self.menu)
        return self.keyboard


def stage_list(num: int, handler: list):
    if len(handler) == 1:
        all_handler = handler[0]
        for i in range(1, num, 1):
            handler.append(all_handler)
    list_out = []
    for i in range(0, num, 1):
        list_out.append(CallbackQueryHandler(handler[i], pattern='^' + str((i + 1)) + '$'))
    LOGGER.info(list_out)
    return list_out


def choose(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    LOGGER.info(f"Owner '{user.first_name}' is Editing 'config.env'")
    update.message.reply_text(text="Select a Environment Variable:", reply_markup=InlineKeyboardMaker(env_name).build(1))
    return FIRST


def view(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    button_list = ['Edit', 'Back']
    env_index = int(query.data) - 1
    env_str = f'{env_name[env_index]} = {env_value[env_index]}'
    query.edit_message_text(text=env_str, reply_markup=InlineKeyboardMaker(button_list).build(2))
    return SECOND


def edit(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    button_list = ['Update', 'Back']
    reply_str = f'Enter New Value:'
    query.edit_message_text(text=reply_str, reply_markup=InlineKeyboardMaker(button_list).build(2))
    return THIRD


def save_changes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reformatter.handler('config.env')
    # sync.handler(file_name, file_id, usePatch=False, update=update, context=context)
    req_restart_msg = f"Please /{BotCommands.RestartCommand} to load changes made to 'config.env'"
    LOGGER.info(req_restart_msg)
    query.edit_message_text(text=req_restart_msg)
    return ConversationHandler.END


def discard_changes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Discarded Changes")
    return FOURTH


def choose_again(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Select a Environment Variable:", reply_markup=InlineKeyboardMaker(env_name).build(1))
    return FIRST


def end(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Exit")
    return ConversationHandler.END


LOGGER = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH = range(4)
file_name = 'config.env'
file_id = fileIdDict[file_name.upper().replace('.', '_')]
env_name, env_value = load_dat(file_name)
# global option
# option: int

conv_handler = ConversationHandler(
        entry_points=[CommandHandler(BotCommands.ConfigCommand, choose, filters=CustomFilters.owner_filter)],
        states={
            # ZEROTH
            # Choose Environment Variable
            FIRST: stage_list(len(env_name), [view]),
            # Show Existing Value
            SECOND: stage_list(2, [edit, choose_again]),
            # Capture New Value for Environment Variable
            THIRD: stage_list(2, [save_changes, discard_changes]),
            # To Save or Discard Changes
            FOURTH: stage_list(2, [choose_again, end]),
            # To Start Over or Exit
        },
        conversation_timeout=180,
        fallbacks=[CommandHandler(BotCommands.ConfigCommand, choose, filters=CustomFilters.owner_filter)]
    )
