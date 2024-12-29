from telethon import TelegramClient, errors
from datetime import datetime, timedelta
import asyncio
import os

api_id = '27983745'  # Ваш api_id
api_hash = 'a759bf1bb3f1201663fc904b7fb97967'  # Ваш api_hash
phone = '+380995541018'  # Ваш номер телефона

session_name = "my_telegram_session_" + str(os.getpid())  # Уникальное имя сессии
client = TelegramClient(session_name, api_id, api_hash)

groups = [
    'https://t.me/+vnczmKn9ih83ZGRi',
    'https://t.me/+DqEK3yaFi6w5MWRi',
    'https://t.me/+7TjyaHrMLTowMzMy',
]
message = "Доброе утро! Это автоматическое сообщение."
file_path = "./test.txt"  # Путь к файлу для отправки

# Асинхронная функция для отправки сообщений и файлов
async def send_message_today():
    await client.start(phone)  # Запуск клиента
    print("Клиент запущен и авторизован.")

    # Цель: отправить сообщение каждый день в 8:00 утра
    while True:
        now = datetime.now()
        send_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

        # Если текущее время уже позже 8:00, отправляем на следующий день
        if now > send_time:
            send_time = send_time + timedelta(days=1)

        # Ждем до 8:00 следующего дня
        time_to_wait = (send_time - now).total_seconds()
        print(f"Ожидание до {send_time}. Время ожидания: {time_to_wait} секунд.")
        await asyncio.sleep(time_to_wait)  # Задержка до следующего дня

        # Отправка сообщений и файлов в группы
        for group_link in groups:
            try:
                group = await client.get_entity(group_link)

                # Отправляем сообщение
                await client.send_message(group, message)
                print(f"Сообщение отправлено в {group_link}!")

                # Отправляем файл
                await client.send_file(group, file_path)
                print(f"Файл отправлен в {group_link}!")

            except errors.RpcError as e:
                print(f"Ошибка при отправке в {group_link}: {e}")
            except Exception as e:
                print(f"Неизвестная ошибка при отправке в {group_link}: {e}")

        print("Сообщение отправлено в 8:00 утра!")

# Запуск основного цикла
async def main():
    async with client:
        await send_message_today()

# Запуск основного цикла
asyncio.run(main())
