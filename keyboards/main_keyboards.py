from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# КЛАВИАТУРА
buttons = ('/Меню', 'Показать расходы', 'Расходы за месяц', 'Удалить данные')
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(buttons[0]).row(buttons[1], buttons[2], buttons[3])
inl_kb = InlineKeyboardMarkup(row_width=1)
inlButton = InlineKeyboardButton(text= 'Подтвердить', callback_data= 'delete_all_data')
inl_kb.add(inlButton)