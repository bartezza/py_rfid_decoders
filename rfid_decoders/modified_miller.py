
from .decoder_utils import group_bits, get_zero_gap_sizes


def decode_modified_miller(bits: str, verbose: bool = False) -> str:

    cc = group_bits(bits)

    if verbose:
        print("cc:", cc)

    cc2, counts = get_zero_gap_sizes(cc)
    # the last count can be longer than the long gap
    assert len(counts) == 3 or len(counts) == 4, counts

    if verbose:
        print("cc2:", cc2)
        print("counts:", counts)

    count_base = counts[0]
    counts = [float(c) / count_base for c in counts]
    th_1 = 1.2
    th_2 = 1.8

    if verbose:
        print("counts:", counts)

    # Short gap --> 0 or a Start if the previous bit was 0, a Start, or nothing
    # Short gap --> 1 if the previous bit was 1
    # Medium gap --> 1 if the previous bit was 0 or a Start
    # Medium gap --> 00 if the previous bit was 1
    # Long gap --> 01 (the previous bit is always 1)
    # When a gap is converted, the resulting bits include the bit to which the short pause following the gap (that triggered the conversion) belongs.

    # The START of the frame is indicated by a logical 0, and its END by a logical 0 followed by a 1111 sequence.

    out_bits = ""
    for c in cc2:
        c = float(c) / count_base
        if c < th_1:
            # short gap
            if verbose:
                print("short ", end="")
            if len(out_bits) == 0 or out_bits[-1] == "0":
                out_bits += "0"
            else:
                out_bits += "1"
        elif c < th_2:
            # medium gap
            if verbose:
                print("med ", end="")
            if len(out_bits) == 0 or out_bits[-1] == "0":
                out_bits += "1"
            else:
                out_bits += "00"
        else:
            # long gap
            if verbose:
                print("long ", end="")
            out_bits += "01"

    if verbose:
        print(out_bits)

    # the Short frame: 7 bits, only for the REQA or WUPA commands
    # ==> S |b0|b1|b2|b3|b4|b5|b6| E
    # the Standard frame: n x (8 bits + 1 bit of odd parity)
    # ==> S |b0|b1|b2|b3|b4|b5|b6|b7| P |b8|b9|b10|b11|b12|b13|b14|b15| P | ... | E

    # start bit
    # assert out_bits[0] == "0"
    # out_bits = out_bits[1:]

    # end bits
    # assert out_bits[-1] == "1"
    # assert out_bits[-2] == "0"
    #out_bits = out_bits[:-2]

    return out_bits
