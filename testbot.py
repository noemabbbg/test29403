import os
import re
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
#5891232930
# Замените 'TOKEN' на токен вашего бота
TOKEN = '5914655297:AAG2ofuc8IpWqPYsgmK-4DLz7Y_Gr5-B5tQ'
db_path = 'ani_test1.sqlite'

# Создаем соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаем таблицу, если ее нет
cursor.execute('''CREATE TABLE IF NOT EXISTS videos
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   series INTEGER,
                   file_id TEXT)''')
conn.commit()

# Создаем объект бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обработчик отправленных видео
@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    video_file = message.video.file_id
    video_name = message.caption

    # Извлекаем имя и серию из названия файла
    match = re.match(r'^(.*?)_\[(\d{2})\]_', video_name)
    if match:
        name = match.group(1)
        series = int(match.group(2))
    else:
        name = video_name
        series = None

    # Сохраняем данные в базу данных
    cursor.execute("INSERT INTO videos (name, series, file_id) VALUES (?, ?, ?)", (name, series, video_file))
    conn.commit()

    await message.answer(f'Видео принято и сохранено в базе данных.\n name:{name}\n series: {series}')




@dp.message_handler(commands='Upload', state = None)
async def add_name(message: types.message):
    if message.from_user.id == '5891232930':



        pass
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
