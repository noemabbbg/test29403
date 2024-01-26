from torrentp import TorrentDownloader
from torrentp import Downloader
import os
import ffmpeg
import re
import asyncio
from agent_sender import AgentSender
import logging
import datetime


# Настройка логирования
logging.basicConfig(filename='conversion.log', level=logging.INFO)

async def MkvToMp4(input_folder):
    output_folder = './preobr'

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.mkv'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp4')

            try:
                # Получение размера преобразуемого файла
                file_size = os.path.getsize(input_file)
                logging.info(f"Размер файла для преобразования: {file_size} байт")

                # Логирование начала преобразования
                logging.info(f"Начато преобразование файла: {input_file}")

                # Преобразование формата с использованием ffmpeg
                process = ffmpeg.input(input_file).output(output_file).run_async(overwrite_output=True)

                # Дождемся завершения процесса
                await process.wait()

                # Получение информации о видео с помощью ffprobe
                probe_result = ffmpeg.probe(output_file, v='error_return')

                # Получение длительности, ширины и высоты видео
                duration = float(probe_result['format']['duration'])
                width = int(probe_result['streams'][0]['width'])
                height = int(probe_result['streams'][0]['height'])

                # Логирование длительности, ширины и высоты видео
                logging.info(f"Длительность видео: {duration} секунд")
                logging.info(f"Ширина видео: {width} пикселей")
                logging.info(f"Высота видео: {height} пикселей")

                # Отправка файла после преобразования
                await AgentSender(output_file, duration, width, height)

                # Логирование завершения преобразования
                logging.info(f"Преобразование файла завершено. Результат: {output_file}")

            except Exception as e:
                logging.error(f"Ошибка при преобразовании файла: {str(e)}")


async def TorrentDownload():
    today_date = datetime.now().strftime("%Y-%m-%d")
    directory_path = os.path.join('.', 'torrentlinks', today_date)
    input_folder = directory_path

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.torrent'):
            print(f"Начата загрузка торрента: {os.path.join(input_folder, file_name)}")

            # Загрузка торрента
            torrent_file = TorrentDownloader(os.path.join(input_folder, file_name), './downloadedTitles')
            torrent_file.start_download()

            # Получение пути к загруженному файлу
            file_name = f'./downloadedTitles/{Downloader.file_nn_path}'
            print(f"Файл торрента загружен. Путь: {file_name}")

            # Вызов функции MkvToMp4 для преобразования
            await MkvToMp4(file_name)


if __name__ == "__main__":
    asyncio.run(TorrentDownload())


