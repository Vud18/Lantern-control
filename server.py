from aiohttp import web

import asyncio


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print('Websocket connection ready')
    flashlight_control_commands = [{b'\x12\x00\x00'}, {b' \x00\x03\xff\xff\xf4'},
                                    {b' \x00\x03\0x91\0x79\0xe7'}, {b'\x13\x00\x00'}]

    for command in flashlight_control_commands:
        await asyncio.sleep(2)
        for byte_number in command:
            print(f"sending: {byte_number}")
            await ws.send_bytes(byte_number)
            print(f"sent: {byte_number}")

    await ws.close()
    print('websocket connection closed')
    return ws


def main():
    app = web.Application()
    app.add_routes([web.get("/", websocket_handler)])
    web.run_app(app, host="127.0.0.1", port=9998)


if __name__ == '__main__':
    main()
