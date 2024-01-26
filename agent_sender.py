import asyncio
import aiohttp
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import os 
import os
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import config

async def AgentSender(file_path):
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

        client.start(phone=phone)
        await client.start()
        file_name = os.path.basename(file_path)
        chat_id = config.chat_id
        object_id = 'argv[4]'
        bot_name = config.bot_name
        mimetypes.add_type('video/mp4', '.mp4')
        print(f'start upload video {file_name}')
        msg = await client.send_file(
            str(bot_name),
            file_path,
            caption=file_name,
            file_name=str(file_name),
            use_cache=False,
            part_size_kb=512,
            attributes=[DocumentAttributeAudio(title=file_name[:-4], performer='')]
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        await client.disconnect()



#if __name__ == "__main__":
 #   asyncio.run(main())
