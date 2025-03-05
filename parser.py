import asyncio
from telethon import TelegramClient, events
from ratelimit import limits, sleep_and_retry

import db
from handlers import bot

# Замените на ваши данные
api_id = 29342701
api_hash = '2a787bbfa265f4300efdeaf1d9a6db87'
phone_number = '+79605319172'

# Список username чатов для парсинга
chat_usernames = ['@test_bota_parser', '@biznes_chat', '@tilda_chat'] # Замените на usernames ваших чатов

# Ключевые слова для поиска
keywords = ['ищу', 'заявка', 'ищем', "нужен", "нужны", "кто может", "кто сможет"]

# Ограничение запросов (например, 1 запрос в секунду)
@sleep_and_retry
@limits(calls=5, period=1)
async def limited_get_sender(event):
    return await event.get_sender()

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)

    # Получаем entity всех чатов из списка
    chats = []
    for username in chat_usernames:
        chat = await client.get_entity(username)
        chats.append(chat)

    @client.on(events.NewMessage(chats=chats)) # Используем список entity чатов
    async def handler(event):
        message_text = event.text.lower()
        for keyword in keywords:
            if keyword in message_text:
                sender = await limited_get_sender(event)
                print(f'Найдено сообщение с ключевым словом "{keyword}" в чате {event.chat.title}:')
                print(f'Отправитель: {sender.first_name} {sender.last_name} (@{sender.username})')
                print(f'Сообщение: {event.text}\n')
                if sender.username not in [None, 'None']:
                    users = db.getAllUsers()
                    l = 0
                    for user in users:
                        l += 1
                        await bot.send_message(user.tg_id, f"{message_text}, @{sender.username}")
                    print(f'Заявку получило {l} пользовате(ль/ей)')
                break

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())