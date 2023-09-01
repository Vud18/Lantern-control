from struct import *


def parse_tlv(data):
    """
    function for encoding from tlv format
    :param data: tlv array
    :return: encode tlv
    """
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


def lamp_control_knob(s):
    res = parse_tlv(s)
    if res['type'] == 0x12 and res['length'] == 0:
        return f'Фонарь включен!'
    if res['type'] == 0x13 and res['length'] == 0:
        return f'Фонарь выключен!'
    if res['type'] == 0x20:
        return f"RGB:{res['value']}"
