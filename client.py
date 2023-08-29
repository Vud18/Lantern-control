import asyncio
import aiohttp
from encode_tlv import lamp_control_knob


async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://localhost:9998/') as ws:

        async for message in ws:
            if message.type == aiohttp.WSMsgType.BINARY:
                result = lamp_control_knob(message.data)
                print(result)

            elif message.type == aiohttp.WSMsgType.CLOSED:
                break
            elif message.type == aiohttp.WSMsgType.ERROR:
                break

    print('websocket connection closed')
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
