from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Категории", callback_data="categories")],
    [InlineKeyboardButton(text="Подписаться", callback_data="buy")],
    [InlineKeyboardButton(text="Справка", callback_data="help")],
    #[InlineKeyboardButton(text="Поддержка", url="https://t.me/reqsearch_support_bot")], #TODO
    [InlineKeyboardButton(text="Поддержка", url="https://t.me/zhdanov_ph")],
]

back_to_menu = [
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

help_menu = [
    [InlineKeyboardButton(text="Как работает бот", callback_data="help1")],
    [InlineKeyboardButton(text="О категориях", callback_data="help2")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

help_back = [
    [InlineKeyboardButton(text="Назад", callback_data="help")]
]

admin = [
    [InlineKeyboardButton(text="Разработка", callback_data="admin_menu1")],
    [InlineKeyboardButton(text="Маркетинг", callback_data="admin_menu2")],
    [InlineKeyboardButton(text="Дизайн", callback_data="admin_menu3")],
    [InlineKeyboardButton(text="Копирайтинг", callback_data="admin_menu4")],
    [InlineKeyboardButton(text="Видеоконтент", callback_data="admin_menu5")],
    [InlineKeyboardButton(text="Продюссирование", callback_data="admin_menu6")],
    [InlineKeyboardButton(text="Разное", callback_data="admin_menu7")],
    [InlineKeyboardButton(text="Продлить подписку", callback_data="buy")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

load_post = [
    [InlineKeyboardButton(text="Загрузить заявку", callback_data="load_post")]
]

categories = [
    [InlineKeyboardButton(text="Разработка", callback_data="sub_menu1")],
    [InlineKeyboardButton(text="Маркетинг", callback_data="sub_menu2")],
    [InlineKeyboardButton(text="Дизайн", callback_data="sub_menu3")],
    [InlineKeyboardButton(text="SMM", callback_data="sub_menu4")],
    [InlineKeyboardButton(text="Наставничество", callback_data="sub_menu5")],
    [InlineKeyboardButton(text="Продюссирование", callback_data="sub_menu6")],
    [InlineKeyboardButton(text="Разное", callback_data="sub_menu6")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

back_to_cat = [
    [InlineKeyboardButton(text="Назад", callback_data="categories")]
]

categories = InlineKeyboardMarkup(inline_keyboard=categories)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
back_to_menu = InlineKeyboardMarkup(inline_keyboard=back_to_menu)
admin = InlineKeyboardMarkup(inline_keyboard=admin)
load_post = InlineKeyboardMarkup(inline_keyboard=load_post)
back_to_cat = InlineKeyboardMarkup(inline_keyboard=back_to_cat)
help_menu = InlineKeyboardMarkup(inline_keyboard=help_menu)
help_back = InlineKeyboardMarkup(inline_keyboard=help_back)
