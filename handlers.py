from aiogram import types, F, Router
from aiogram import Bot
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder

import payment_process
import random, math
import config
import kb, db
import text
import datetime
from datetime import timedelta
import os
import uuid

from yookassa import Configuration, Payment

from funcs import days_until_date, sub_date, decline_day, buy_sub

router = Router()
bot = Bot(token=config.BOT_TOKEN)

class Form(StatesGroup):
    menu = State()
    admin = State()
    post = State()
    buying = State()

@router.message(F.text == "Старт")
@router.message(F.text == "Начать")
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(text=text.start, reply_markup=kb.menu)

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(text.help, reply_markup=kb.help_menu)

@router.callback_query(F.data == "help")
async def help_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.help, reply_markup=kb.help_menu)

@router.callback_query(F.data == "help1")
async def help_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.about, reply_markup=kb.help_back)

@router.callback_query(F.data == "help2")
async def help_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.cat_help, reply_markup=kb.help_back)

@router.message(Command("exit"))
async def exit(state: FSMContext):
    await state.menu()

@router.callback_query(F.data == "menu")
async def menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.menu, reply_markup=kb.menu)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(text=text.start, reply_markup=kb.menu)

#оплата

temp_payments = {} #в продакшене заменить на бд

Configuration.account_id = config.YOOKASSA_SHOP_ID
Configuration.secret_key = config.YOOKASSA_SECRET_KEY

@router.callback_query(F.data == "buy")
async def handle_payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    payment = Payment.create({
        "amount": {"value": "500.00", "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/zhdanov_ph_test1_bot"
        },
        "description": "Подписка на 1 месяц",
        "metadata": {"user_id": callback_query.message.from_user.id}
    }, str(uuid.uuid4()))

    temp_payments[payment.id] = {
        "user_id": callback_query.message.from_user.id,
        "status": payment.status,
        "created_at": datetime.datetime.now(),
        "amount": payment.amount.value
    }

    await callback_query.message.answer(f"Оплатите 500 руб. {payment.confirmation.confirmation_url}")
    if await payment_process.check_payment_status_enhanced(payment.id):
        payment = Payment.find_one(payment.id)
        if payment.status == "waiting_for_capture":
            idempotence_key = str(uuid.uuid4())
            response = Payment.capture(
                payment.id,
                {
                    "amount": {
                        "value": f"{payment['amount']['value']}",
                        "currency": "RUB"
                    }
                },
                idempotence_key
            )
        await callback_query.message.answer("Платёж прошёл успешно, поздравляем!", reply_markup=kb.back_to_menu)
        await buy_sub(callback_query.message.from_user.id, callback_query.message.from_user.username, payment.captured_at)
        await db.addPayment(callback_query.message.from_user.id, callback_query.message.from_user.username, payment.id)
    else:
        await callback_query.message.answer("Платёж прошёл неудачно, попробуйте ещё раз или напишите в поддержку", reply_markup=kb.back_to_menu)

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
    users = db.getUsersByCat(data['load_type'])
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
    if user.type1 != 0:
        texts[0] += f" (Выбрана)"
    if user.type2 != 0:
        texts[1] += f" (Выбрана)"
    if user.type3 != 0:
        texts[2] += f" (Выбрана)"
    if user.type4 != 0:
        texts[3] += f" (Выбрана)"
    if user.type5 != 0:
        texts[4] += f" (Выбрана)"
    if user.type6 != 0:
        texts[5] += f" (Выбрана)"
    if user.type7 != 0:
        texts[6] += f" (Выбрана)"

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
    sub = db.checkSubscription(user.tg_id)

    if sub:
        days_until = math.ceil(days_until_date(sub.end_date))
        if days_until > 0:
            await callback_query.message.edit_text(f"""<b>{decline_day(days_until)} подписки</b>""", reply_markup=categories)
        else:
            await callback_query.message.edit_text(f"""<b>Подписка не оформлена</b>""", reply_markup=categories)
    else:
        await callback_query.message.edit_text(f"""<b>Подписка не оформлена</b>""", reply_markup=categories)


@router.callback_query(F.data == "sub_menu1")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type1 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type1=0)

            print('already', user_id, username, user)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type2 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type2=0)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type3 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type3=0)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type4 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type4=0)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type5 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type5=0)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type6 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type6=0)
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type7 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            db.rewriteUser(user_id, username, type7=0)
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
    users = db.getUsersByCat(data['load_type'])
    l = 0
    for user in users:
        l += 1
        await bot.send_message(user.tg_id, f"{message.text}, @{message.forward_from.username}")
    await message.answer(f"({l} пользовател(ь/ей) получило заявку), \n{text.post_loaded}",  reply_markup=kb.admin)



