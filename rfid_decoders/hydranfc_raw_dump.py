
from typing import List
from .decoder_utils import show_bin_str


class HydraNFCDump:
    filename: str
    raw_32bit: List[str]
    raw_downsampled: List[str]
    packets: List[dict]

    # packet = {"data": raw_32bit_data, "bits": str, "type": str}

    @staticmethod
    def load_raw_mod_dump(filename: str) -> "HydraNFCDump":
        """
        Load a raw (modified) dump of a sniff session with HydraNFC.
        Modified-raw dumps contains:
         - raw stream of 32bits entries, in hex notation
         - downsampled stream of 8bits entries, in hex notation
        Entries are separated by spaces or new-lines.
        """

        # read all the data
        with open(filename, "r") as fp:
            data2 = fp.readlines()
        # remove spaces
        data2 = [d.strip() for d in data2]
        # build list of raw entries
        data = []
        for dd in data2:
            data += dd.split(" ")
        # print(data)
        # divide entries in raw 32bit and downsampled ones
        dump = HydraNFCDump()
        dump.filename = filename
        dump.raw_32bit = [d for d in data if len(d) == 8]
        dump.raw_downsampled = [d for d in data if len(d) == 2]

        # divide into packets
        # NOTE: this is very hacky and experimental!
        raw1 = dump.raw_32bit
        packets = []
        cur = 0
        last_packet_end = None
        while cur < len(raw1) - 1:
            waiting = None
            found = None
            for i in range(cur, len(raw1) - 1):
                if not waiting:
                    if (raw1[i] == "00000000" and raw1[i + 1] == "00000000"):
                        waiting = 1
                    elif (raw1[i] == "ffffffff" and raw1[i + 1] == "ffffffff"):
                        waiting = 2
                elif waiting == 1:
                    if raw1[i] != "00000000":
                        found = 1
                        print(f"Found start of frame at {i} (1)")
                        break
                elif waiting == 2:
                    if raw1[i] != "ffffffff":
                        found = 2
                        print(f"Found start of frame at {i} (2)")
                        break

            # extract packet
            if found == 1:
                packet = {
                    "data": raw1[cur:i],
                    "bits": HydraNFCDump.raw_32bit_to_bitstream(raw1[cur:i]),
                    "type": "1"
                }
                packets.append(packet)
                # advance
                last_packet_end = i - 1
                cur = i
            elif found == 2:
                packet = {
                    "data": raw1[cur:i],
                    "bits": HydraNFCDump.raw_32bit_to_bitstream(raw1[cur:i]),
                    "type": "2"
                }
                packets.append(packet)
                # advance
                last_packet_end = i - 1
                cur = i
            else:
                # advance
                cur = i + 1

        # rem = HydraNFCDump.raw_32bit_to_bitstream(raw1[last_packet_end:]) if last_packet_end is not None else None
        rem = raw1[last_packet_end:] if last_packet_end is not None else None
        print(f"{len(packets)} packets found, remaining = '{rem}'")
        dump.packets = packets
        return dump

    @staticmethod
    def raw_32bit_to_bitstream(raw: List[str]) -> str:
        bits = ""
        for i in range(len(raw) - 1):
            d = raw[i]
            # print(d)
            b4 = show_bin_str(int(d[0:2], 16))
            b3 = show_bin_str(int(d[2:4], 16))
            b2 = show_bin_str(int(d[4:6], 16))
            b1 = show_bin_str(int(d[6:8], 16))
            # bits += b1[::-1] + b2[::-1] + b3[::-1] + b4[::-1]
            bits += (b1 + b2 + b3 + b4)  # [::-1]
            # if raw[i - 1] == "ffffffff" and raw[i] == "ffffffff":
            #     break
            # if raw[i - 1] == "00000000" and raw[i] == "00000000":
            #     break
        return bits
