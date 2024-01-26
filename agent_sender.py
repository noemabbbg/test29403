import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import mimetypes
import config


import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import mimetypes
import config
import ffmpeg

async def AgentSender():
    entity = 'asdasdads'
    api_id = config.api_id
    api_hash = config.api_hash
    phone = config.phone
    client = TelegramClient(entity, api_id, api_hash)

    try:
        await client.connect()
        await client.start(phone=phone)

        preobr_folder = './preobr'

        for file_name in os.listdir(preobr_folder):
            if file_name.endswith('.mp4'):
                file_path = os.path.join(preobr_folder, file_name)

                # Get video properties using ffmpeg
                probe = ffmpeg.probe(file_path, v='error')
                video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

                duration = float(video_info['duration'])
                width = video_info['width']
                height = video_info['height']

                chat_id = config.chat_id
                bot_name = config.bot_name

                # Add support for different media types (in this case - video)
                mimetypes.add_type('video/mp4', '.mp4')

                print(f'Start upload video {file_name}')

                # Upload file with duration, width, and height attributes
                await client.send_file(
                    str(bot_name),
                    file_path,
                    caption=file_name,
                    file_name=str(file_name),
                    use_cache=False,
                    part_size_kb=512,
                    attributes=[DocumentAttributeVideo(duration=duration, w=width, h=height)]
                )

                print(f'Upload completed for {file_name}')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        await client.disconnect()

