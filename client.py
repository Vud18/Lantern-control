import asyncio
import aiohttp
import argparse
from encode_tlv import lamp_control_knob


async def main():
    session = aiohttp.ClientSession()
    args = connection_method_argparse()
    async with session.ws_connect(f'http://{args.indir}:{args.outdir}/') as ws:

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


def connection_method_argparse():
    """
    The function is designed to enter through the console command, using the host and port method
    :return:
    """
    parser = argparse.ArgumentParser(description='host and port')
    parser.add_argument('indir', type=str, help='You need to enter a host and port. Input example: 127.0.0.1 9999')
    parser.add_argument('outdir', type=int)
    args = parser.parse_args()

    if args.indir == '127.0.0.1' and args.outdir == 9999:
        print('Host: 127.0.0.1. Port: 9999')
    else:
        print("Something is entered incorrectly!")

    return args


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()
