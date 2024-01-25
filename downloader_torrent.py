from torrentp import TorrentDownloader
from torrentp import Downloader
import os
import ffmpeg
import re
import asyncio
from agent_sender import AgentSender



async def MkvToMp4(input_folder):
    output_folder = './preobr' #надо создавать папку с названием анимехи ну или потом
    for file_name in os.listdir(input_folder): # соотвественно перебор сначала папок и того что внутри
        if file_name.endswith('.mkv'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp4')
            print(output_file)# Преобразование формата с использованием ffmpeg
            ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)
            print(output_file)
            await AgentSender(output_file)
            # хз че по завершению но логирование + статус выполнения хоть какой то нужно

async def TorrentDownload():
    input_folder = './torrentLinks'
    for file_name in os.listdir(input_folder):
        print(file_name)
        if file_name.endswith('.torrent'):
            print(f' Начата загрузка:{os.path.join(input_folder, file_name)}')
            torrent_file = TorrentDownloader(os.path.join(input_folder, file_name), './downloadedTitles')
            torrent_file.start_download()
            file_name = f'./downloadedTitles/{Downloader.file_nn_path}'
            print(f'1234567{file_name}')
            await MkvToMp4(file_name)




if __name__ == "__main__":
    asyncio.run(TorrentDownload())


