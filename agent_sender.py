import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import mimetypes
import config


async def AgentSender():
    entity = 'asdasdads'
    api_id = config.api_id
    api_hash = config.api_hash
    phone = config.phone
    client = TelegramClient(entity, api_id, api_hash)

    try:
        await client.connect()

        '''
        if not client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter code: '))
        '''

        await client.start(phone=phone)
        #await client.start()

        preobr_folder = './preobr'

        for file_name in os.listdir(preobr_folder):
            if file_name.endswith('.mp4'):
                file_path = os.path.join(preobr_folder, file_name)

                chat_id = config.chat_id
                bot_name = config.bot_name

                # Добавляем поддержку разных типов медиа (в данном случае - видео)
                mimetypes.add_type('video/mp4', '.mp4')

                print(f'Start upload video {file_name}')

                # Отправляем файл
                await client.send_file(
                    str(bot_name),
                    file_path,
                    caption=file_name,
                    file_name=str(file_name),
                    use_cache=False,
                    part_size_kb=512,
                    attributes=[DocumentAttributeVideo()]
                )

                print(f'Upload completed for {file_name}')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(AgentSender())
