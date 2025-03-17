from aiogram import types, F, Router
from aiogram import Bot
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder

import random
import config
import kb, db
import text
import datetime

router = Router()
bot = Bot(token=config.BOT_TOKEN)

def sub_date():
    """
      Получает текущую дату и время, прибавляет 30 дней и возвращает результат в виде строки.
      """
    today = datetime.datetime.now()
    dateplus = today + datetime.timedelta(days=30)
    return dateplus.strftime("%Y-%m-%d")  # Форматируем в строку в формате год-месяц-день

def days_until_date(date_string):
  try:
    target_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()  # Convert the string to a date object
  except ValueError:
    print("Error: Invalid date format. Use '%Y-%m-%d'.")
    return None

  today = datetime.date.today()  # Get the current date (without time)
  difference = target_date - today  # Calculate the difference between the dates

  return difference.days  # Return the number of days in the difference

def decline_day(number):
  """
  Declines the word "day" and adds the appropriate "left" phrase according to Russian grammar.

  Args:
    number: An integer.

  Returns:
    A string containing the "left" phrase, the number, and the declined word "day".
  """
  remainder_10 = number % 10
  remainder_100 = number % 100

  if remainder_10 == 1 and remainder_100 != 11:
    word = "день"
    left_word = "остался"
  elif 2 <= remainder_10 <= 4 and (remainder_100 < 10 or remainder_100 >= 20):
    word = "дня"
    left_word = "осталось"
  else:
    word = "дней"
    left_word = "осталось"

  return f"{left_word} {number} {word}"


class Form(StatesGroup):
    menu = State()
    admin = State()
    post = State()

@router.message(F.text == "Старт")
@router.message(F.text == "Начать")
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(text=text.start, reply_markup=kb.menu)

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(text.help, reply_markup=kb.back_to_menu)

@router.message(Command("exit"))
async def exit(state: FSMContext):
    await state.menu()

@router.callback_query(F.data == "menu")
async def menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.menu, reply_markup=kb.menu)

#Админка

@router.callback_query(F.data == "admin_back")
async def menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if data['admin'] == 'yes':
        await callback_query.message.edit_text(text.admin, reply_markup=kb.admin)
    else:
        await callback_query.message.edit_text('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    if message.from_user.username in config.admin_list:
        await message.answer(text.admin, reply_markup=kb.admin)
        await state.update_data({'admin':'yes', 'tg_id': message.from_user.id},)
    else:
        await message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu1")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 1})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu2")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 2})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu3")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 3})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu4")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 4})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu5")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 5})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu6")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 6})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu7")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 7})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu8")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 8})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu9")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 9})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "admin_menu10")
async def admin1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    if callback_query.from_user.username in config.admin_list:
        await state.update_data({'admin': 'yes', 'tg_id': callback_query.from_user.id, 'load_type': 10})
        await callback_query.message.edit_text(text.load_post)
        await state.set_state(Form.post)
    else:
        await callback_query.message.answer('Ошибка: Вы не являетесь администратором', reply_markup=kb.back_to_menu)


@router.message(Form.post)
async def load_post(message: Message, state: FSMContext):
    data = await state.get_data()
    users = db.getUsersBySub(data['load_type'])
    l = 0
    for user in users:
        l += 1
        await bot.send_message(user.tg_id, f"{message.text}, @{message.forward_from.username}")
    await message.answer(f"({l} пользовател(ь/ей) получило заявку), \n{text.post_loaded}",  reply_markup=kb.admin)

#Категории

@router.callback_query(F.data == "categories")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    uid = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(uid)
    if user is None:
        db.addUser(uid, username)
    user = db.getUserByTgID(uid)
    texts = ["Разработка", "Маркетинг", "Дизайн", "Копирайтинг", "Видеоконтент", "Продюссирование", "Разное", "Назад"]
    type1, type2, type3, type4, type5, type6, type7, type8, type9, type10 = days_until_date(user.type1), days_until_date(user.type2), days_until_date(user.type3), days_until_date(user.type4), days_until_date(user.type5), days_until_date(user.type6), days_until_date(user.type7), days_until_date(user.type8), days_until_date(user.type9), days_until_date(user.type10)
    if type1 is not None:
        texts[0] += f" ({decline_day(type1)})"
    if type2 is not None:
        texts[1] += f" ({decline_day(type2)})"
    if type3 is not None:
        texts[2] += f" ({decline_day(type3)})"
    if type4 is not None:
        texts[3] += f" ({decline_day(type4)})"
    if type5 is not None:
        texts[4] += f" ({decline_day(type5)})"
    if type6 is not None:
        texts[5] += f" ({decline_day(type6)})"
    if type7 is not None:
        texts[6] += f" ({decline_day(type7)})"

    categories = [
        [InlineKeyboardButton(text=texts[0], callback_data="sub_menu1")],
        [InlineKeyboardButton(text=texts[1], callback_data="sub_menu2")],
        [InlineKeyboardButton(text=texts[2], callback_data="sub_menu3")],
        [InlineKeyboardButton(text=texts[3], callback_data="sub_menu4")],
        [InlineKeyboardButton(text=texts[4], callback_data="sub_menu5")],
        [InlineKeyboardButton(text=texts[5], callback_data="sub_menu6")],
        [InlineKeyboardButton(text=texts[6], callback_data="sub_menu7")],
        [InlineKeyboardButton(text=texts[7], callback_data="menu")]
    ]
    categories = InlineKeyboardMarkup(inline_keyboard=categories)
    await callback_query.message.edit_text(text.cat, reply_markup=categories)

@router.callback_query(F.data == "sub_menu1")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type1) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type1=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub1, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type1=type)
        print('add')
        await callback_query.message.edit_text(text.sub1, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu2")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type2) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type2=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub2, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type2=type)
        print('add')
        await callback_query.message.edit_text(text.sub2, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu3")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type3) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type3=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub3, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type3=type)
        print('add')
        await callback_query.message.edit_text(text.sub3, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu4")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type4) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type4=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub4, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type4=type)
        print('add')
        await callback_query.message.edit_text(text.sub4, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu5")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type5) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type5=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub5, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type5=type)
        print('add')
        await callback_query.message.edit_text(text.sub5, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu6")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type6) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type6=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub6, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type6=type)
        print('add')
        await callback_query.message.edit_text(text.sub6, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu7")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = sub_date()
    print("User_By_ID", user)
    if user:
        if days_until_date(user.type7) is not None:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type7=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub7, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type7=type)
        print('add')
        await callback_query.message.edit_text(text.sub7, reply_markup=kb.back_to_cat)


@router.message(Form.post)
async def load_post(message: Message, state: FSMContext):
    data = await state.get_data()
    users = db.getUsersBySub(data['load_type'])
    l = 0
    for user in users:
        l += 1
        await bot.send_message(user.tg_id, f"{message.text}, @{message.forward_from.username}")
    await message.answer(f"({l} пользовател(ь/ей) получило заявку), \n{text.post_loaded}",  reply_markup=kb.admin)



@router.callback_query(F.data == "faq")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.faq, reply_markup=kb.back_to_menu)
