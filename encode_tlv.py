from struct import *


def parse_tlv(data):
    index = 0
    while index < len(data):
        t = data[index]
        index += 1

        l = int.from_bytes(data[index:index + 2], byteorder='big')
        index += 2

        if len(data[index:index + l]) == 3:
            v = unpack('>BBB', data[index:index + l])
            index += l
            return {'type': t, 'length': l, 'value': v}
        else:
            index += l
            return {'type': t, 'length': l}


def lamp_control_knob(s):
    res = parse_tlv(s)
    if res['type'] == 0x12 and res['length'] == 0:
        return f'Фонарь включен!'
    if res['type'] == 0x13 and res['length'] == 0:
        return f'Фонарь выключен!'
    if res['type'] == 0x20:
        return f"RGB:{res['value']}"
