# py_rfid_decoders

Experimental decoders for protocols used in RFID transmissions from raw captured data.

Supported dump formats:

 - List of 32bit hex values captured with HydraNFC using raw sniff mode (modified to not downsample the signal)

Supported decoders:
 
 - Modified Miller (for PCD -> PICC communications for Type A tags)
  
Decoding of ISO14443 frames is also supported.

The code is in its first version and it is highly experimental.
Therefore, it is likely filled with bugs and it could probably be re-implemented in a much better way.
