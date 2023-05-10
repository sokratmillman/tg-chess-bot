from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts import AGREE_TEXT, DISAGREE_TEXT

button_agree = KeyboardButton(AGREE_TEXT)
button_disagree = KeyboardButton(DISAGREE_TEXT)

accept_invite_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
accept_invite_kb.row(button_agree, button_disagree)
