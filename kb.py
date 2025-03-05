from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Подписаться на категорию заявок", callback_data="categories")],
    [InlineKeyboardButton(text="Личный кабинет", callback_data="cabinet")],
    [InlineKeyboardButton(text="Поддержка", callback_data="support")],
   # [InlineKeyboardButton(text="FAQ", callback_data="faq")]
]

back_to_menu = [
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

admin = [
    [InlineKeyboardButton(text="SEO", callback_data="admin_menu1")],
    [InlineKeyboardButton(text="SMM", callback_data="admin_menu2")],
    [InlineKeyboardButton(text="Видеомонтаж", callback_data="admin_menu3")],
    [InlineKeyboardButton(text="Дизайн", callback_data="admin_menu4")],
    [InlineKeyboardButton(text="Контекст", callback_data="admin_menu5")],
    [InlineKeyboardButton(text="Копирайтинг", callback_data="admin_menu6")],
    [InlineKeyboardButton(text="Продюсирование", callback_data="admin_menu7")],
    [InlineKeyboardButton(text="Разработка", callback_data="admin_menu8")],
    [InlineKeyboardButton(text="Сайт", callback_data="admin_menu9")],
    [InlineKeyboardButton(text="Таргет", callback_data="admin_menu10")],
    [InlineKeyboardButton(text="Ответить как техподдержка", callback_data="support_reply")],
    [InlineKeyboardButton(text="Назад", callback_data="menu")]
]

load_post = [
    [InlineKeyboardButton(text="Загрузить заявку", callback_data="load_post")]
]

categories = [
    [InlineKeyboardButton(text="SEO", callback_data="sub_menu1")],
    [InlineKeyboardButton(text="SMM", callback_data="sub_menu2")],
    [InlineKeyboardButton(text="Видеомонтаж", callback_data="sub_menu3")],
    [InlineKeyboardButton(text="Дизайн", callback_data="sub_menu4")],
    [InlineKeyboardButton(text="Контекст", callback_data="sub_menu5")],
    [InlineKeyboardButton(text="Копирайтинг", callback_data="sub_menu6")],
    [InlineKeyboardButton(text="Продюсирование", callback_data="sub_menu7")],
    [InlineKeyboardButton(text="Разработка", callback_data="sub_menu8")],
    [InlineKeyboardButton(text="Сайт", callback_data="sub_menu9")],
    [InlineKeyboardButton(text="Таргет", callback_data="sub_menu10")],
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