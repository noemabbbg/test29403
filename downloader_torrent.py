from torrentp import TorrentDownloader
from torrentp import Downloader
import os
import ffmpeg
import re
import asyncio
from agent_sender import AgentSender
import logging


# Настройка логирования
logging.basicConfig(filename='conversion.log', level=logging.INFO)

async def MkvToMp4(input_folder):
    output_folder = './preobr'

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.mkv'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp4')

            # Логирование начала преобразования
            logging.info(f"Начато преобразование файла: {input_file}")

            # Преобразование формата с использованием ffmpeg
            ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)

            # Логирование завершения преобразования
            logging.info(f"Преобразование файла завершено. Результат: {output_file}")

            # Отправка файла после преобразования
            await AgentSender(output_file)

async def TorrentDownload():
    input_folder = './torrentLinks'

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.torrent'):
            logging.info(f"Начата загрузка торрента: {os.path.join(input_folder, file_name)}")

            # Загрузка торрента
            torrent_file = TorrentDownloader(os.path.join(input_folder, file_name), './downloadedTitles')
            torrent_file.start_download()

            # Получение пути к загруженному файлу
            file_name = f'./downloadedTitles/{Downloader.file_nn_path}'
            logging.info(f"Файл торрента загружен. Путь: {file_name}")

            # Вызов функции MkvToMp4 для преобразования
            await MkvToMp4(file_name)


if __name__ == "__main__":
    asyncio.run(TorrentDownload())


