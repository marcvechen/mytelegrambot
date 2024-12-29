from telethon import TelegramClient, errors
from datetime import datetime, timedelta
import asyncio
import time

# Вставь свои данные
api_id = '27983745'  # Полученный api_id
api_hash = 'a759bf1bb3f1201663fc904b7fb97967'  # Полученный api_hash
phone = '+380995541018'  # Телефонный номер (в международном формате, например: +380XXXXXXXXX)

# Создание клиента
client = TelegramClient('my_telegram_session.session', api_id, api_hash)

# Список чатов и файл для отправки
groups = [
    'https://t.me/+vnczmKn9ih83ZGRi',  # Первая группа
    'https://t.me/+DqEK3yaFi6w5MWRi',   # Ещё одна группа
    'https://t.me/+7TjyaHrMLTowMzMy',  # Ещё одна группа
]
message = "Доброе утро! Это автоматическое сообщение."
file_path = "./test.txt"  # Путь к файлу, который ты хочешь отправить

# Асинхронная функция для отправки сообщений и файлов
async def send_message_daily():
    await client.start(phone)  # Запуск клиента
    print("Клиент запущен и авторизован.")

    while True:
        now = datetime.now()

        # Проверка, что сегодня рабочий день (с понедельника по пятницу)
        if now.weekday() < 5:
            send_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

            # Если текущее время меньше времени отправки, ждем до 8:00
            if now < send_time:
                wait_time = (send_time - now).seconds
                print(f"Ждем {wait_time} секунд до отправки сообщения.")
                time.sleep(wait_time)  # Ждем до 8:00

            # Отправка сообщений и файлов в группы
            for group_link in groups:
                try:
                    # Получаем объект группы
                    group = await client.get_entity(group_link)

                    # Отправляем сообщение
                    await client.send_message(group, message)
                    print(f"Сообщение отправлено в {group_link}!")

                    # Отправляем файл (если он существует)
                    await client.send_file(group, file_path)
                    print(f"Файл отправлен в {group_link}!")

                except errors.RpcError as e:
                    print(f"Ошибка при отправке в {group_link}: {e}")
                except Exception as e:
                    print(f"Неизвестная ошибка при отправке в {group_link}: {e}")

            print("Сообщение отправлено в 8:00!")

        # Ждем 24 часа, чтобы проверить снова
        print("Ждем до следующего дня...")
        time.sleep(86400)  # Ждем 24 часа (86400 секунд)

# Запуск основного цикла
with client:
    client.loop.run_until_complete(send_message_daily())
