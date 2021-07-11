
from pathlib import Path
from rfid_decoders.hydranfc_raw_dump import HydraNFCDump
from rfid_decoders.modified_miller import decode_modified_miller
from rfid_decoders.manchester import decode_manchester
from rfid_decoders.framing import decode_framing
from rfid_decoders.decoder_utils import split_bitstream, bitstream_to_bytes,\
    dump_hex_array


cur_dir = Path(__file__).resolve().parent
filename = cur_dir.parent / "dumps" / "dump_raw1_typeA.txt"

dump = HydraNFCDump.load_raw_mod_dump(filename=filename)

# print(dump.raw_32bit)

# print(json.dumps(dump.packets, indent=4))

for idx, p in enumerate(dump.packets):
    if p["type"] == "2":
        continue  # skip

        print(f"\n==== Packet {idx} ====")

        bits = p["bits"]
        out_bits = decode_modified_miller(bits, verbose=True)

        print(split_bitstream(out_bits, 8))

        bytes = decode_framing(out_bits)

        # bytes = bitstream_to_bytes(out_bits)
        ret = dump_hex_array(bytes)

        print(ret)

    elif p["type"] == "1" and idx == 3:

        print(f"\n==== Packet {idx} ====")

        bits = p["bits"]
        
        out_bits = decode_manchester(bits, verbose=True)

        print(split_bitstream(out_bits, 8))

        bytes = decode_framing(out_bits)

        # bytes = bitstream_to_bytes(out_bits)
        ret = dump_hex_array(bytes)

        print(ret)

        break  # TEMP
