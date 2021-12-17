# Day 16

import binascii
import numpy as np

with open('../input.txt') as f:
    packet = f.readlines()[0].strip()
    packet = binascii.unhexlify(packet)
    packet = "".join([bin(p)[2:].zfill(8) for p in packet])

def split(packet, i, parse=True):
    return int(packet[:i], 2) if parse else packet[:i], packet[i:]

operators = {
    0: np.sum,
    1: np.product,
    2: np.min,
    3: np.max,
    5: lambda values: int(values[0] > values[1]),
    6: lambda values: int(values[0] < values[1]),
    7: lambda values: int(values[0] == values[1])
}

version_sum = 0

def parse_packet(packet):
    version, packet = split(packet, 3)
    type_id, packet = split(packet, 3)

    global version_sum
    version_sum += version

    if type_id == 4:
        num = ""
        while True:
            group, packet = split(packet, 5, False)
            num += group[1:]
            if group[0] == '0':
                break
        return int(num, 2), packet

    else: # Operator
        length, packet = split(packet, 1)
        values = []
        if length == 0:
            num_bits, packet = split(packet, 15)
            target_len = len(packet) - num_bits
            while len(packet) > target_len:
                result, packet = parse_packet(packet)
                values.append(result)
        else:
            num_packets, packet = split(packet, 11)
            for _ in range(num_packets):
                result, packet = parse_packet(packet)
                values.append(result)

        return operators[type_id](values), packet


print("Part 2:", parse_packet(packet)[0])
print("Part 1:", version_sum)