import importlib
import re
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

from tg_bot import dispatcher, updater, TOKEN, WEBHOOK, OWNER_ID, DONATION_LINK, CERT_PATH, PORT, URL, LOGGER, \
    ALLOW_EXCL
# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from tg_bot.modules import ALL_MODULES
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.misc import paginate_modules

PM_START_TEXT = """
ഹായ് {}, എന്റെ പേര് {}! 
എന്തുണ്ടെങ്കിലും ഗ്രൂപ്പിൽ ചോദിച്ചാൽ മതി😓

@movie_Cafe_2
"""

HELP_STRINGS = """
Bഉളുപ്പില്ലേ  മറ്റുള്ളവരുടെ ബോട്ടിൽ പണിയാൻ 🙄
എന്നെ നിങ്ങളുടെ ഗ്രൂപ്പിൽ ആഡ് ചെയ്യാൻ നോക്കി സമയം കളയണ്ട, എന്നെ ♻️movie Cafe♻️ ഗ്രൂപ്പിൽ മാത്രമേ ആഡ് ചെയ്യാൻ കഴിയൂ...!!!


