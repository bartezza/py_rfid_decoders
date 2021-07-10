
from pathlib import Path
from rfid_decoders.hydranfc_raw_dump import HydraNFCDump
from rfid_decoders.modified_miller import decode_modified_miller
from rfid_decoders.framing import decode_framing
from rfid_decoders.decoder_utils import dump_hex_array


def test_pcd_decoding(request):
    # Sent bits:     26 (7 bits)
    # Received bits: 04  00   
    # Sent bits:     93  20  
    # Received bits: 3e  f9  fc  9f  a4  
    # Sent bits:     93  70  3e  f9  fc  9f  a4  91  b2  
    # Received bits: 08  b6  dd  
    # Sent bits:     50  00  57  cd

    values = {
        0: "26",
        2: "93 20",
        4: "93 70 3e f9 fc 9f a4 91 b2",
        6: "50 00 57 cd"
    }

    cur_dir = Path(request.fspath).parent if request else Path(".").resolve()
    filename = cur_dir.parent / "dumps" / "dump_raw1_typeA.txt"

    dump = HydraNFCDump.load_raw_mod_dump(filename=filename)
    
    # print(dump.raw_32bit)

    # print(json.dumps(dump.packets, indent=4))
    # print(dump.packets[2]["bits"])

    for idx, packet in enumerate(dump.packets):
        if packet["type"] != "2":
            continue

        print(f"\n=== Packet {idx} ===")
        print(f"Num data = {len(packet['data'])}, type = {packet['type']}")
        # print(packet["data"])
        print(packet["bits"])

        bits = packet["bits"]
        out_bits = decode_modified_miller(bits, verbose=True)
        bytes = decode_framing(out_bits)
        ret = dump_hex_array(bytes)

        print(ret)
        assert ret == values[idx], values[idx]


if __name__ == "__main__":
    test_pcd_decoding(None)
