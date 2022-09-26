

import os
import base64
mssg="90"
key='7e1a0bbc8c770667be44dce10c'

for j in range (0,16):
    indx=(hex(j)[2:4]).upper()
    if(indx==2): #### Als dats d'exemple no surt
        break
    IVx='0'+indx
    f=open('bytes_'+IVx+'FFxx.txt','w')
    for i in range(0,256):
        value_hex=(hex(i)[2:4]).upper()
        if(len(value_hex)==1):
            value_hex='0'+value_hex
        IV=IVx+"FF"+value_hex
        key_with_IV=IV+key
        print(key_with_IV)
        command="echo -n '"+mssg+"' | openssl enc -K '"+key_with_IV+"' -rc4 | xxd"
        out=os.popen(command).read()
        print(repr(out))
        keystream=out.split(': ')[-1]
        cipher_message= ((keystream.split('    ')[0]).split(' '))[-1]
        f.write(IV +" "+cipher_message[2:4]+"\n")
        print(IV,cipher_message[2:4])
