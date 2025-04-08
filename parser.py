import asyncio
import datetime

from telethon import TelegramClient, events
from ratelimit import limits, sleep_and_retry
from funcs import days_until_date

import db
from handlers import bot

# Замените на ваши данные
api_id = 21595524
api_hash = 'ca0d8d57af7def888cb0ebf07c856cb6'
phone_number = '+79012999757'

# Список username чатов для парсинга
chat_usernames = ['@test_bota_parser', '@biznes_chat', '@tilda_chat'] # Замените на usernames ваших чатов

# Пользователи, сообщения от которых не попадают в заявки ни при каких условиях
banned_users = []

# Ключевые слова для поиска
keywords = ['ищу', 'заявка', 'ищем', "нужен", "нужны", "кто может", "кто сможет", "в поисках"]
cat_keywords = {
    "1": ["программист", "разработчик","frontend","backend","fullstack","python","javaScript","1c", "1с","веб-разработка", "сайт", "вёрстка", "верстальщик", "tilda", "wordpress", "разработка", "приложение", "мобильное приложение", "программирование", "backend", "frontend", "fullstack", "API", "интеграция", "бот", "скрипт", "автоматизация", "база данных", "CRM", "1С", "парсер", "парсинг", "сбор данных", "оптимизация", "хостинг", "деплой", "алгоритм", "blockchain", "смарт-контракт", "нейросет", "ML"],
    "2": ["маркетолог", "таргетолог", "smm", "смм", "контекстная реклама", "seo", "копирайтер", "контент-маркетинг", "контент маркетинг" ,"продвижение", "продвижения","pr", "email-маркетинг", "email маркетинг", "маркетинг", "таргет", "таргетированная реклама", "контекстная реклама", "SEO", "продвижение", "SMM", "воронка продаж", "лидогенерация", "трафик", "конверсия", "CPA", "CPC", "ROI", "Google Analytics", "Яндекс.Метрика", "email-рассылка", "медийная реклама", "брендинг", "аудит", "конкурентный анализ", "вирусный маркетинг", "партнерка", "вебинар"],
    "3": ["дизайнер", "дизайн", "логотип", "фирменный стиль", "брендбук", "айдентика", "UI/UX", "мокап", "презентаци", "баннер", "иллюстраци", "графика", "графику", "полиграф", "визитк", "мерч", "упаковк", "шрифт", "типографика", "3D", "обложк", "шаблон", "редактура фото", "ретушь", "коллаж", "лого", "иконки", "стикеры", "NFT"],
    "4": ["копирайтер", "копирайтинг", "текст", "статья", "пост", "рерайт", "SEO-текст", "рекламный текст", "продающий текст", "слоган", "описание", "контент-план", "email-рассылка", "новости", "пресс-релиз", "отзыв", "обзор", "скрипт", "стилизация", "перевод", "корректура", "редактура", "нейминг", "игра слов", "сторителлинг", "UX-текст", "микрокопирайтинг"],
    "5": ["видео", "видеомейкер", "рилсмейкер", "видео", "монтаж", "ролик", "тизер", "обзор", "анимация", "моушн-дизайн", "титры", "субтитры", "озвучка", "закадровый голос", "цветокоррекция", "спецэффекты", "VFX", "клип", "стрим", "YouTube", "TikTok", "Reels", "Shorts", "сторис", "интро", "аутро", "таймкод", "хромакей", "раскадровка", "сценарий", "видеоблог", "трейлер"],
    "6": ["продюсер", "продюссирование", "продюсирование", "проект", "организация", "запуск", "управление", "координация", "подбор команды", "бюджет", "тайм-менеджмент", "контроль", "логистика", "ивент", "мероприятие", "концерт", "подкаст", "шоу", "трансляция", "продакшн", "агент", "менеджмент", "права", "контракт", "переговоры", "бренд-партнерство", "спонсорство", "рекламная интеграция", "аутсорс", "фриланс-координация"]
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
                        db.addRequest(cat, message_text, sender.username, datetime.datetime.now().strftime("YYYY-MM-DD HH:MM:SS"))
                        subs = db.getSubscriptions()
                        user_ids = [sub.tg_id for sub in subs if days_until_date(sub.end_date) > 0]
                        user_ids2 = db.getUsersIdByCat(cat)
                        l = 0
                        for user_id in user_ids:
                            if user_id in user_ids2:
                                l += 1
                                await bot.send_message(user_id, f"<b>Заявка: {text_cat}</b> \n\n{message_text}\n\n <b>Контакт:</b> @{sender.username}")
                        print(f'Заявку получило {l} пользовате(ль/ей)')
                    break

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())