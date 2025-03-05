from aiogram import types, F, Router
from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder

import random
import config
import kb, db
import text

router = Router()
bot = Bot(token=config.BOT_TOKEN)

class Form(StatesGroup):
    menu = State()
    admin = State()
    post = State()
    support_reply = State()
    support_send = State()

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
    await callback_query.message.edit_text(text.cat, reply_markup=kb.categories)

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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type2 == type:
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type3 == type:
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type4 == type:
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type5 == type:
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type6 == type:
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
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type7 == type:
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

@router.callback_query(F.data == "sub_menu8")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type8 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type8=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub8, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type8=type)
        print('add')
        await callback_query.message.edit_text(text.sub8, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu9")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type9 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type9=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub9, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type9=type)
        print('add')
        await callback_query.message.edit_text(text.sub9, reply_markup=kb.back_to_cat)

@router.callback_query(F.data == "sub_menu10")
async def admin1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = db.getUserByTgID(user_id)
    type = 1
    print("User_By_ID", user)
    if user:
        if user.type10 == type:
            await callback_query.message.edit_text(text.cat_already, reply_markup=kb.back_to_cat)
            print('already')
        else:
            db.rewriteUser(user_id, username, type10=type)
            print('rewrite')
            await callback_query.message.edit_text(text.sub10, reply_markup=kb.back_to_cat)
    else:
        db.addUser(user_id, username, type10=type)
        print('add')
        await callback_query.message.edit_text(text.sub10, reply_markup=kb.back_to_cat)


@router.callback_query(F.data == "cabinet")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text.cab, reply_markup=kb.back_to_menu)

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
