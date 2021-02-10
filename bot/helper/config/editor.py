import logging
import warnings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ConversationHandler, CallbackContext, CallbackQueryHandler, MessageHandler
from telegram.ext import Filters
from . import reformatter
from .load import load_dat, file_bak, update_dat
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters


class InlineKeyboardMaker:
    def __init__(self, button_list: list):
        self.button_list = button_list
        self.buttons = []
        self.menu = []
        self.keyboard = []

    def build(self, columns: int):
        for i in range(len(self.button_list)):
            self.buttons.append(InlineKeyboardButton(text=self.button_list[i], callback_data=(i + 1)))
        self.menu = [self.buttons[i:i + columns] for i in range(0, len(self.buttons), columns)]
        self.keyboard = InlineKeyboardMarkup(self.menu)
        return self.keyboard


def stage_list(num: int, handler: list):
    if len(handler) == 1:
        all_handler = handler[0]
        for i in range(num - 1):
            handler.append(all_handler)
    list_out = []
    for i in range(num):
        list_out.append(CallbackQueryHandler(handler[i], pattern='^' + str(i + 1) + '$'))
    return list_out


def choose(update: Update, context: CallbackContext) -> None:
    global env_name, env_value, env_name_new, env_value_new, temp_index, temp_value
    env_name, env_value, env_name_new, env_value_new = [], [], [], []
    temp_index, temp_value = '', ''
    LOGGER.info(f"Owner '{update.message.from_user.first_name}' is Editing 'config.env'")
    env_name, env_value = load_dat(file_bak(CONFIG_ENV_FILE))
    reply_str = "Select an Environment Variable:"
    update.message.reply_text(text=reply_str, reply_markup=InlineKeyboardMaker(env_name).build(1))
    return FIRST


def choose_again(update: Update, context: CallbackContext) -> None:
    global temp_index, temp_value
    temp_index, temp_value = '', ''
    query = update.callback_query
    query.answer()
    reply_str = "Select an Environment Variable:"
    query.edit_message_text(text=reply_str, reply_markup=InlineKeyboardMaker(env_name).build(1))
    return FIRST


def view(update: Update, context: CallbackContext) -> None:
    global temp_index
    query = update.callback_query
    query.answer()
    button_list = ['Edit', 'Back']
    temp_index = f'{int(query.data) - 1}'
    env_str = f'{env_name[int(temp_index)]} = {env_value[int(temp_index)]}'
    query.edit_message_text(text=env_str, reply_markup=InlineKeyboardMaker(button_list).build(2))
    return SECOND


def edit(update: Update, context: CallbackContext) -> None:
    global temp_index
    query = update.callback_query
    query.answer()
    button_list = ['Ok', 'Back']
    reply_str = f'Send New Value for {env_name[int(temp_index)]}:'
    query.edit_message_text(text=reply_str, reply_markup=InlineKeyboardMaker(button_list).build(2))
    return THIRD


def new_val(update: Update, context: CallbackContext) -> None:
    global temp_value
    temp_value = update.message['text']


def verify(update: Update, context: CallbackContext) -> None:
    global temp_value
    query = update.callback_query
    query.answer()
    button_list = ['Update Value', 'Back']
    reply_str = f'Entered Value is:\n\n{temp_value}'
    query.edit_message_text(text=reply_str, reply_markup=InlineKeyboardMaker(button_list).build(2))
    return FOURTH


def proceed(update: Update, context: CallbackContext) -> None:
    global env_name, env_name_new, env_value_new, temp_index, temp_value
    env_name_new_already_exists = False
    for i in range(len(env_name_new)):
        if env_name[int(temp_index)] == env_name_new[i]:
            env_name_new_already_exists = True
            env_value_new[i] = temp_value
            pass
    if env_name_new_already_exists is False:
        env_name_new.append(env_name[int(temp_index)])
        env_value_new.append(temp_value)
    query = update.callback_query
    query.answer()
    button_list = ['Save Changes', 'Discard Changes', 'Change Another Value']
    reply_str = ''
    for i in range(len(env_name_new)):
        reply_str = reply_str + f'{env_name_new[i]} = {env_value_new[i]}' + '\n'
    query.edit_message_text(text=reply_str, reply_markup=InlineKeyboardMaker(button_list).build(1))
    return FIFTH


def discard_changes(update: Update, context: CallbackContext) -> None:
    global env_name_new, env_value_new
    env_name_new, env_value_new = [], []
    query = update.callback_query
    query.answer()
    button_list = ['Start Over', 'Exit']
    LOGGER.info(f"Owner '{update.callback_query.from_user.first_name}' Discarded Changes Made to 'config.env'")
    query.edit_message_text(text=f"Discarded Changes", reply_markup=InlineKeyboardMaker(button_list).build(2))
    return SIXTH


def save_changes(update: Update, context: CallbackContext) -> None:
    global env_name_new, env_value_new
    query = update.callback_query
    query.answer()
    reformatter.handler(CONFIG_ENV_FILE)
    for i in range(len(env_name_new)):
        update_dat(CONFIG_ENV_FILE, env_name_new[i], env_value_new[i])
    LOGGER.info(f"Owner '{update.callback_query.from_user.first_name}' Saved Changes Made to 'config.env'")
    reply_str = f"Saved Changes.\nPlease /{BotCommands.RestartCommand} to Sync Changes made to 'config.env'."
    query.edit_message_text(text=reply_str)
    return ConversationHandler.END


def end(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Exited 'config.env' Editor.")
    return ConversationHandler.END


LOGGER = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH = range(6)
CONFIG_ENV_FILE = 'config.env'
env_name: list
env_value: list
env_name_new: list
env_value_new: list
temp_index: str
temp_value: str

handler = ConversationHandler(
    entry_points=[CommandHandler(BotCommands.ConfigCommand, choose, filters=CustomFilters.owner_filter)],
    states={
        # ZEROTH
        # Choose Environment Variable
        FIRST: stage_list(len(open(CONFIG_ENV_FILE, 'r').readlines()), [view]),
        # Show Existing Value
        SECOND: stage_list(2, [edit, choose_again]),
        # Capture New Value for Environment Variable
        THIRD: stage_list(2, [verify, edit]) + [MessageHandler(Filters.text, new_val)],
        # Verify New Value
        FOURTH: stage_list(2, [proceed, choose_again]),
        # Show All Changes and Proceed
        FIFTH: stage_list(3, [save_changes, discard_changes, choose_again]),
        # Save or Discard Changes
        SIXTH: stage_list(2, [choose_again, end])
        # Exit or Start Over
    },
    fallbacks=[CommandHandler(BotCommands.ConfigCommand, choose, filters=CustomFilters.owner_filter)],
    conversation_timeout=120
)
