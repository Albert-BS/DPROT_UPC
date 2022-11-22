import os
import sys

if len(sys.argv) != 2:
    print("Usage: \n python3 keygen.py <name to generate the keys for")
    exit()

name = sys.argv[1]

# Generate param file
os.system("openssl genpkey -genparam -algorithm dh -pkeyopt dh_rfc5114:3 -out param.pem")

# Key generation and public key extraction
os.system("openssl genpkey -paramfile param.pem -out " + name + "_pkey.pem")
os.system("openssl pkey -in " + name + "_pkey.pem -pubout -out " + name + "_pubkey.pem")