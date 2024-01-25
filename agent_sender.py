import asyncio
import aiohttp
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import os 
async def AgentSender(file_path):
    entity = 'asdasdads'
    api_id = 28694336
    api_hash = '221b4605366bdb25d548b0b122f26ca2'
    phone = '+79950698150'

    client = TelegramClient(entity, api_id, api_hash)

    await client.connect()

    # Uncomment the following line for the first run, then comment it to avoid FloodWait
   # await client.send_code_request(phone)

   # await client.sign_in(phone, input('Enter code: '))
    await client.start()
    file_name = os.path.basename(file_path)
    chat_id = '5914655297'
    object_id = 'argv[4]'
    bot_name = 'egbooxoem_bot'
    duration = '3'

    mimetypes.add_type('video/mp4', '.mp4')
    print('111')
    msg = await client.send_file(
        str(bot_name),
        file_path,
        caption=file_name,
        file_name=str(file_name),
        use_cache=False,
        part_size_kb=512,
        attributes=[DocumentAttributeAudio(
            int(duration),
            voice=None,
            title=file_name[:-4],
            performer='')]
    )

    await client.disconnect()
    return 0

#if __name__ == "__main__":
 #   asyncio.run(main())
