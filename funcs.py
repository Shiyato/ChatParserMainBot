import datetime

import db

def sub_date(date):
    """
      Получает текущую дату и время, прибавляет 30 дней и возвращает результат в виде строки.
      """
    if not date:
        today = datetime.datetime.now()
    else:
        today = date
    dateplus = today + datetime.timedelta(days=30)
    return dateplus.strftime('%Y-%m-%d %H:%M:%S')

def days_until_date(date_string):
  target_date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()

  today = datetime.date.today()  # Get the current date (without time)
  difference = target_date - today  # Calculate the difference between the dates

  return difference.total_seconds() / 86400  # 86400 секунд в дне

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
    left_word = "Остался"
  elif 2 <= remainder_10 <= 4 and (remainder_100 < 10 or remainder_100 >= 20):
    word = "дня"
    left_word = "Осталось"
  else:
    word = "дней"
    left_word = "Осталось"

  return f"{left_word} {number} {word}"

def buy_sub(tg_id:str, username:str, start_date:str):
    sub = db.checkSubscription(tg_id)
    if sub:
        if days_until_date(sub.end_date) <= 0:
            print('Продлеваем подписку1')
            db.rewriteSubscription(tg_id, username, sub_date(datetime.strptime(sub.end_date)))
        else:
            print('Продлеваем подписку2')
            db.rewriteSubscription(tg_id, username, sub_date(datetime.now()))
    else:
        print('Оформляем подписку')
        db.addSubscription(tg_id=tg_id, username=username, start_date=start_date, end_date=sub_date(datetime.strptime(start_date)))