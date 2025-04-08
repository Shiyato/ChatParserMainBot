import asyncio
from yookassa import Payment
from datetime import datetime, timedelta



async def check_payment_status_enhanced(
        payment_id: str,
        interval: float = 1.0,
        timeout: float = 600.0,
        verbose: bool = True
):
    """
    Улучшенная версия с настройками интервала и времени проверки

    :param payment_id: ID платежа
    :param interval: Интервал проверки в секундах (по умолчанию 1 сек)
    :param timeout: Максимальное время проверки в секундах (по умолч. 300 = 5 мин)
    :param verbose: Вывод логов в консоль
    :return: Статус платежа
    """
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=timeout)

    while datetime.now() < end_time:
        try:
            payment = Payment.find_one(payment_id)

            if payment.status == 'waiting_for_capture':
                if verbose:
                    print(f"Платеж {payment_id} подтвержден!")
                return True

            elif payment.status == 'succeeded':
                if verbose:
                    print(f"Платеж {payment_id} подтвержден!")
                return True

            elif payment.status in ('canceled', 'failed'):
                if verbose:
                    print(f"Платеж {payment_id} отменен/неудачен")
                return False

            if verbose:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Статус: {payment.status}")

        except Exception as e:
            if verbose:
                print(f"Ошибка запроса: {str(e)}")

        await asyncio.sleep(interval)

    if verbose:
        print(f"Платеж не подтвержден за {timeout} секунд")
    return False