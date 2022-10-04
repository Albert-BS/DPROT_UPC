import os
import base64

mssg = 'm'
key = '666d3abd482b70a112f82ffd4b'

for j in range(1, 16):
    indx = (hex(j)[2:4]).upper()
    if indx != "2":     # IV = 02FFXX not useful
        IVx = '0' + indx
        f = open('bytes_' + IVx + 'FFxx.dat', 'w')
        for i in range(0, 256):
            value_hex = (hex(i)[2:]).upper()
            if len(value_hex) == 1:
                value_hex = '0' + value_hex
            IV = IVx + "FF" + value_hex
            key_with_IV = IV + key
            command = "echo -n '" + mssg + "' | openssl enc -K '" + key_with_IV + "' -rc4 | xxd"
            out = os.popen(command).read()
            keystream = out[10] + out[11] # Last two corresponding to the m[0]
            f.write("0X" + IV.upper() + " 0X" + keystream.upper() + "\n")
