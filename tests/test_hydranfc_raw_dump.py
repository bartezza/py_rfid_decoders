
import json
from pathlib import Path
from rfid_decoders.hydranfc_raw_dump import HydraNFCDump


def test_hydranfc_raw_dump(request):
    cur_dir = Path(request.fspath).parent if request else Path(".").resolve()
    filename = cur_dir.parent / "dumps" / "dump_raw1_typeA.txt"

    dump = HydraNFCDump.load_raw_mod_dump(filename=filename)
    
    # print(dump.raw_32bit)

    # print(json.dumps(dump.packets, indent=4))
    # print(dump.packets[2]["bits"])

    for idx, packet in enumerate(dump.packets):
        print(f"\n=== Packet {idx} ===")
        print(f"Num data = {len(packet['data'])}, type = {packet['type']}")
        print(packet["data"])


if __name__ == "__main__":
    test_hydranfc_raw_dump(None)
