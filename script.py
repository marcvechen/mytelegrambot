import asyncio
import os
from telethon import TelegramClient, errors

# Установи свои данные
api_id = '27983745'
api_hash = 'a759bf1bb3f1201663fc904b7fb97967'

# Список групп, файлов и путей к файлам с текстом
groups = [
    {'link': 'https://t.me/+vnczmKn9ih83ZGRi', 'message_file': './text.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+DqEK3yaFi6w5MWRi', 'message_file': './text2.txt', 'file': './file2.pdf'},
    {'link': 'https://t.me/+7TjyaHrMLTowMzMy', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+Yqdf5moWCPwxMGE6', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+9wIhttGM3fplYTE6', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+etV5Fe5EHBhhNGE6', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+dVUHIsB1NA5iYzFi', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+spVnUhd8IsJjYzAy', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+ypshIqR6_UMxYmUy', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+gdeTyFyUEgYyOWQy', 'message_file': './text3.txt', 'file': './file1.pdf'},
    {'link': 'https://t.me/+taC5O6uvjkE3ZDMy', 'message_file': './text3.txt', 'file': './file1.pdf'},
]

# Создание клиента
client = TelegramClient('my_telegram_session', api_id, api_hash)

async def send_message_and_file(group):
    try:
        # Читаем текст из файла
        if os.path.exists(group['message_file']):
            with open(group['message_file'], 'r', encoding='utf-8') as f:
                message = f.read()
        else:
            print(f"Файл с текстом {group['message_file']} не найден.")
            return

        # Получаем объект группы
        group_entity = await client.get_entity(group['link'])

        # Отправляем сообщение
        await client.send_message(group_entity, message)
        print(f"Сообщение отправлено в {group['link']}")

        # Проверяем существование файла
        if group['file'] and os.path.exists(group['file']):
            await client.send_file(group_entity, group['file'])
            print(f"Файл {group['file']} отправлен в {group['link']}")
        else:
            print(f"Файл {group['file']} не найден или не указан для {group['link']}")

    except errors.RPCError as e:
        print(f"Ошибка при отправке в {group['link']}: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка при отправке в {group['link']}: {e}")

async def send_messages_and_files():
    await client.start()
    print("Клиент запущен и авторизован.")

    # Создаём задачи для параллельной отправки
    tasks = [send_message_and_file(group) for group in groups]
    
    # Выполняем все задачи параллельно
    await asyncio.gather(*tasks)

    print("Все сообщения и файлы успешно отправлены!")

# Запуск
with client:
    client.loop.run_until_complete(send_messages_and_files())