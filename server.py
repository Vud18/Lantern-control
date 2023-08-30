from aiohttp import web

import asyncio
import itertools


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    incoming = asyncio.ensure_future(process_incoming_messages(ws))

    for i in itertools.count():
        if ws.closed:
            break
        await asyncio.sleep(4)
        flashlight_control_commands = [{b'\x12\x00\x00'}, {b' \x00\x03\xff\xff\xf4'},
                                       {b' \x00\x03\0x91\0x79\0xe7'}, {b'\x13\x00\x00'}]

        for command in flashlight_control_commands:
            await asyncio.sleep(4)
            for byte_number in command:
                print(f"sending: {byte_number}")
                await ws.send_bytes(byte_number)
                print(f"sent: {byte_number}")

        await ws.close()
        break
    print('websocket connection closed')

    await incoming

    return ws


async def process_incoming_messages(ws):
    async for msg in ws:
        pass


def main():
    app = web.Application()
    app.add_routes([web.get("/", websocket_handler)])
    web.run_app(app, host="127.0.0.1", port=9998)


if __name__ == '__main__':
    main()
