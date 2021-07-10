
from typing import List, Tuple


# dilation
def fill_gaps(bits: str, width: int) -> str:
    bits2 = list(bits)
    for i in range(len(bits) - width):
        if bits[i] == "1" and bits[i + width - 1] == "1":
            for j in range(i + 1, i + width - 1):
                bits2[j] = "1"
    return ''.join(bits2)


def group_bits(bits: str) -> List[Tuple[str, int]]:
    cc = [[bits[0], 0]]
    for b in bits:
        if b == cc[-1][0]:
            cc[-1][1] += 1
        else:
            cc.append([b, 1])
    return cc


def get_zero_gap_sizes(
        cc: List[Tuple[str, int]]) -> Tuple[List[int], List[int]]:
    # cc = result of group_bits(bits)
    cc2 = []
    counts = set()
    for i in range(len(cc) - 1):
        if cc[i][0] == "0":
            assert cc[i + 1][0] == "1"
            cc2.append(cc[i + 1][1])
            counts.add(cc[i + 1][1])
    counts = sorted(list(counts))
    return cc2, counts


def split_bitstream(bits: str, group_size: int) -> List[str]:
    cur = 0
    ret = []
    while cur < len(bits):
        ll = min(cur + group_size, len(bits))
        byt = bits[cur:ll]
        ret.append(byt)
        cur = ll
    return ret


def bitstream_to_bytes(bits: str) -> List[int]:
    bytes = split_bitstream(bits, 8)
    return [
        int(b[::-1], 2)
        for b in bytes
    ]


def show_bin_str(b: int) -> str:
    return (bin(b))[2:].zfill(8)


def hex_to_bin_str(w: str) -> str:
    return show_bin_str(int(w, 16))


def dump_hex_array(bytes: List[int]) -> str:
    ret = ""
    for b in bytes:
        if ret:
            ret += " "
        h = hex(b)[2:]
        if len(h) == 1:
            ret += "0"
        ret += h
    return ret
