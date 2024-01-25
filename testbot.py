import os
import re
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
import config

# Замените 'TOKEN' на токен вашего бота
TOKEN = config.bot_token
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

# Обработчик команды /kb
@dp.message_handler(commands=['kb'])
async def show_keyboard(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    # Получение уникальных значений из столбца name
    cursor.execute("SELECT DISTINCT name FROM videos")
    names = cursor.fetchall()

    for name in names:
        keyboard.add(KeyboardButton(name[0]))

    await message.answer("Выберите видео:", reply_markup=keyboard)

# Обработка нажатия на кнопку с именем
@dp.message_handler(lambda message: message.text in [name[0] for name in cursor.execute("SELECT DISTINCT name FROM videos")])
async def handle_name_button(message: types.Message):
    selected_name = message.text

    # Получение уникальных значений из столбца series для выбранного name
    cursor.execute("SELECT DISTINCT series FROM videos WHERE name=?", (selected_name,))
    series_list = cursor.fetchall()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for series in series_list:
        keyboard.add(KeyboardButton(str(series[0])))

    await message.answer(f"Выберите серию для видео {selected_name}:", reply_markup=keyboard)

# Обработка нажатия на кнопку с серией
@dp.message_handler(lambda message: message.text.isdigit())
async def handle_series_button(message: types.Message):
    selected_series = int(message.text)

    # Получение file_id для выбранной серии
    cursor.execute("SELECT file_id FROM videos WHERE series=?", (selected_series,))
    file_id = cursor.fetchone()

    if file_id:
        await message.answer_video(file_id[0], caption=f"Видео для серии {selected_series}")
    else:
        await message.answer("Файл не найден.")

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


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=None)
async def handle_document(message: types.Message, state: FSMContext):
    user_id_to_accept = config.my_id
    if message.from_user.id == user_id_to_accept:
        document = message.document
        if document.mime_type == 'application/x-bittorrent' and document.file_name.endswith('.torrent'):
            directory_path = './torrentlinks'
            os.makedirs(directory_path, exist_ok=True)
            file_path = os.path.join(directory_path, document.file_name)
            if not os.path.exists(file_path):
                # Сохраняем файл в директорию
                await message.document.download(file_path)

                # Отправляем ответное сообщение
                await message.answer(f"Файл {document.file_name} сохранен в директории {directory_path}")

                # Отправляем клавиатуру после сохранения файла
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                cursor.execute("SELECT DISTINCT name FROM videos")
                names = cursor.fetchall()
                for name in names:
                    keyboard.add(KeyboardButton(name[0]))
                await message.answer("Выберите видео:", reply_markup=keyboard)
            else:
                await message.answer(f"Файл {document.file_name} уже существует в директории {directory_path}")
        else:
            await message.answer("Пожалуйста, отправьте файл типа .torrent")
    else:
        await message.answer("Вы не имеете права отправлять файлы этого типа")

    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
