
from .decoder_utils import group_bits, get_zero_gap_sizes,\
    fill_gaps, show_bin_str, hex_str_to_bitstream


def decode_manchester(bits: str, verbose: bool = False) -> str:

    # Sent bits:     26 (7 bits)
    # Received bits: 04  00   
    # Sent bits:     93  20  
    # Received bits: 3e  f9  fc  9f  a4  
    # Sent bits:     93  70  3e  f9  fc  9f  a4  91  b2  
    # Received bits: 08  b6  dd  
    # Sent bits:     50  00  57  cd 

    # the signal is much noisier from PICC to PCD
    bits = fill_gaps(bits, 3)
    bits = fill_gaps(bits, 4)
    bits = fill_gaps(bits, 5)

    print(bits)

    cc = group_bits(bits)

    if verbose:
        print("cc:", cc)

    # skip the first short groups
    idx = 0
    while cc[idx][1] < 10 and idx < len(cc):
        idx += 1

    print(idx)

    import math

    short_gap_len = None
    long_gap_len = None

    temp_sum = 0.0
    temp_len = 0
    for idx2 in range(idx, len(cc)):
        cur_gap_len = cc[idx2][1]
        if temp_len == 0:
            temp_sum = cur_gap_len
            temp_len += 1
        else:
            # calculate average of encountered gaps
            temp_avg = temp_sum / temp_len
            # calculate factor between cur gap and average
            factor = cur_gap_len / temp_avg
            # check the factor
            if math.fabs(factor - 1.0) < 0.1:  # 10 %
                # if it is close, then the current gap is probably of the
                # same "kind" as the encountered ones, thus add it to the
                # average
                temp_sum += cur_gap_len
                temp_len += 1
            elif math.fabs(factor - 2.0) < 0.1:
                # new gap is twice the average, so it is probably the
                # long gap, while the average is the short gap
                long_gap_len = cur_gap_len
                short_gap_len = round(temp_avg)
                break
            elif math.fabs(factor - 0.5) < 0.05:
                # new gap is half the average, so it is probably the
                # short gap, while the average is the long gap
                short_gap_len = cur_gap_len
                long_gap_len = round(temp_avg)
                break
            else:
                # factor is completely off, we can't do anything
                raise Exception(f"Could not detect short/long gap sizes "
                                f"(factor = {factor})")

    if short_gap_len is None:
        raise Exception("Could not detect short/long gap sizes")
    
    print(f"Long gap = {long_gap_len}, short gap = {short_gap_len}")

    print("3e f9 = {}".format(hex_str_to_bitstream("3e f9")))

    for idx2 in range(idx, len(cc)):
        cur_bit, cur_gap_len = cc[idx2]

        factor = round(cur_gap_len / short_gap_len)
        print(f"{round(factor)} ", end="")

    print("")

    # TODO
    return ""
