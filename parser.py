import asyncio
from telethon import TelegramClient, events
from ratelimit import limits, sleep_and_retry

import db
from handlers import bot

# Замените на ваши данные
api_id = 21595524
api_hash = 'ca0d8d57af7def888cb0ebf07c856cb6'
phone_number = '+79012999757'

# Список username чатов для парсинга
chat_usernames = ['@test_bota_parser', '@biznes_chat', '@tilda_chat'] # Замените на usernames ваших чатов

# Ключевые слова для поиска
keywords = ['ищу', 'заявка', 'ищем', "нужен", "нужны", "кто может", "кто сможет", "в поисках"]
cat_keywords = {
    "1": ["программист", "разработчик","frontend","backend","fullstack", "разработка","python","javaScript","1c", "1с","веб-разработка", "сайт", "вёрстка", "верстальщик", "tilda", "wordpress"],
    "2": ["маркетолог", "таргетолог", "smm", "смм", "контекстная реклама", "seo", "копирайтер", "контент-маркетинг", "контент маркетинг" ,"продвижение", "продвижения","pr", "email-маркетинг", "email маркетинг"],
    "3": ["дизайнер"],
    "4": ["копирайтер"],
    "5": ["видео", "видеомейкер", "рилсмейкер"],
    "6": ["продюсер", "продюссирование"]
}
redflag_words = ['спам', 'спамер', 'бан']

def check_cat(text):
    exit = ''
    for key, wordlist in cat_keywords.items():
        for word in wordlist:
            if word in text:
                exit = key
                break
    return '7' if exit == '' else exit



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

        rf = False
        for redflag in redflag_words:
            if redflag in message_text:
                rf = True
                break

        if not rf:
            for keyword in keywords:
                if keyword in message_text:
                    cat = int(check_cat(message_text))
                    subs_t = ["Разработка", "Маркетинг", "Дизайн", "Копирайтинг", "Видеоконтент", "Продюсирование", "Разное"]
                    text_cat = subs_t[cat-1]
                    sender = await limited_get_sender(event)
                    print(f'Найдено сообщение с ключевым словом "{keyword}" в чате {event.chat.title}:')
                    print(f'Отправитель: {sender.first_name} {sender.last_name} (@{sender.username})')
                    print(f'Сообщение: {event.text}\n')
                    if sender.username not in [None, 'None']:
                        users = db.getUsersBySub(cat)
                        l = 0
                        for user in users:
                            l += 1
                            await bot.send_message(user.tg_id, f"Категория заявки: {text_cat} \n\n{message_text}, @{sender.username}")
                        print(f'Заявку получило {l} пользовате(ль/ей)')
                    break

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())