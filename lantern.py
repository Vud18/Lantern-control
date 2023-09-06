import asyncio
from struct import unpack

import aiohttp
import argparse


_LANTERN_DESCRIPTION = (
    'Управляемый по сети фонарь. '
    'Скрипт подключается к серверу и '
    'обрабатывает получаемые команды управления.'
)

def connection_method_argparse():
    parser = argparse.ArgumentParser(description=_LANTERN_DESCRIPTION)
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    return args


def parse_tlv(data):
    index = 0
    while index < len(data):
        type_tlv = data[index]
        index += 1

        length = int.from_bytes(data[index:index + 2], byteorder='big')
        index += 2

        if len(data[index:index + length]) == 3:
            value = unpack('>BBB', data[index:index + length])
            index += length
            return {'type': type_tlv, 'length': length, 'value': value}
        else:
            index += length
            return {'type': type_tlv, 'length': length}


def process_raw_bytes(s):
    res = parse_tlv(s)
    if res['type'] == 0x12 and res['length'] == 0:
        return f'Фонарь включен!'
    if res['type'] == 0x13 and res['length'] == 0:
        return f'Фонарь выключен!'
    if res['type'] == 0x20:
        return f"RGB:{res['value']}"


async def main():
    session = aiohttp.ClientSession()
    args = connection_method_argparse()
    async with session.ws_connect(f'http://{args.host}:{args.port}/') as ws:

        async for message in ws:
            if message.type == aiohttp.WSMsgType.BINARY:
                result = process_raw_bytes(message.data)
                print(result)
            elif message.type == aiohttp.WSMsgType.CLOSED:
                break
            elif message.type == aiohttp.WSMsgType.ERROR:
                break

    print('websocket connection closed')
    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
