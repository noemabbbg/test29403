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

async def MkvToMp4(dp, input_folder):
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

                # Логирование размера файла каждую секунду
                while process.poll() is None:
                    current_size = os.path.getsize(output_file)
                    logging.info(f"Преобразовано {current_size} байт из {file_size} байт")
                    await asyncio.sleep(1)

                # Логирование завершения преобразования
                logging.info(f"Преобразование файла завершено. Результат: {output_file}")

                # Отправка статуса в телеграм


                # Отправка файла после преобразования
                await AgentSender(output_file)

            except Exception as e:
                logging.error(f"Ошибка при преобразовании файла: {str(e)}")


async def TorrentDownload():
    input_folder = './torrentLinks'

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


