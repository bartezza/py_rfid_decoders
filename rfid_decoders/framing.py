
from typing import List


# the Short frame: 7 bits, only for the REQA or WUPA commands
# ==> S |b0|b1|b2|b3|b4|b5|b6| E
# the Standard frame: n x (8 bits + 1 bit of odd parity)
# ==> S |b0|b1|b2|b3|b4|b5|b6|b7| P |b8|b9|b10|b11|b12|b13|b14|b15| P | ... | E

def decode_framing(bits: str, check_start_bit: bool = False,
                    end_seq: str = "001",
                    end_seq2: str = "01") -> List[int]:
    if check_start_bit:
        # start bit should be 0
        assert bits[0] == "0"
        # start from next bit
        cur = 1
    else:
        # start bit not present in bitstream
        cur = 0
    ret = []
    while cur < len(bits):
        # if cur + 7 + len(end_seq) == len(bits):
        if cur <= 1 and len(bits) < 16:  # euristic!
            # assuming short frame
            ll = min(cur + 7, len(bits))
            byt = bits[cur:ll]
            ret.append(int(byt[::-1], 2))
            print(f"SHORT FRAME {byt}, REM '{bits[cur + 7:]}'")
            # end seq
            assert bits[cur + 7: cur + 7 + len(end_seq)] == end_seq
            return ret

        # is there place for full byte + parity?
        elif cur + 8 <= len(bits):
            # full frame
            ll = min(cur + 8, len(bits))
            byt = bits[cur:ll]
            ret.append(int(byt[::-1], 2))
            # parity
            parity = bits[cur + 8]
            # advance
            cur = ll + 1
            val = hex(int(byt[::-1], 2))[2:]
            print(f"BYTE {byt} ({val}), PARITY {parity}, REM '{bits[cur:]}'")

        elif bits[cur:] == end_seq or bits[cur:] == end_seq2:
            # assuming end sequence
            print(f"END REM '{bits[cur:]}'")
            return ret
        
        # elif cur + len(end_seq) == len(bits):
        #     # assuming end sequence
        #     print(f"END REM '{bits[cur:]}'")
        #     assert bits[cur: cur + len(end_seq)] == end_seq
        #     return ret
        
        else:
            raise Exception("Invalid frame")
    return ret
