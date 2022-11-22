import os

name = input("Introduce the name of the receiver:")
message = input("Introduce the plain message to encrypt:")

if not os.path.isfile("param.pem"):
    print("Missing param.pem file")
    exit()

if not os.path.isfile(name + "_pubkey.pem"):
    print("Missing public key file")
    exit()

# Generate eph keys
os.system("openssl genpkey -paramfile param.pem -out ephpkey.pem")
os.system("openssl pkey -in eph_pkey.pem -pubout -out  ephpubkey.pem")

# Derive common secret
os.system("openssl pkeyutl -inkey ephpkey.pem -peerkey " + name + "_pubkey.pem -derive -out common.bin")

# Obtaining the keys k1 and k2 and generating the IV
os.system("cat common.bin | openssl dgst -sha256 -binary | head -c 16 > k1.bin")
os.system("cat common.bin | openssl dgst -sha256 -binary | tail -c 16 > k2.bin")
os.system("openssl rand 16 > iv.bin")

# Encryption and tag generation
os.system("openssl enc -aes-128-cbc -K `cat k1.bin | xxd -p` -iv `cat iv.bin | xxd -p` -in " + message + " -out ciphertext.bin")
os.system("cat iv.bin ciphertext.bin | openssl dgst -sha256 -binary -mac hmac -macopt hexkey:`cat k2.bin | xxd -p` -out > tag.bin")

# Generate cipher file
os.system("cat ephpubkey.pem > ciphertext.pem")
os.system("echo \"-----BEGIN AES-128-CBC IV-----\" >> ciphertext.pem")
os.system("cat iv.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END AES-128-CBC IV-----\" >> ciphertext.pem")
os.system("echo \"-----BEGIN AES-128-CBC CIPHERTEXT-----\" >> ciphertext.pem")
os.system("cat ciphertext.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END AES-128-CBC CIPHERTEXT-----\" >> ciphertext.pem")
os.system("echo \"-----BEGIN SHA256-HMAC TAG-----\" >> ciphertext.pem")
os.system("cat tag.bin | openssl base64 >> ciphertext.pem")
os.system("echo \"-----END SHA256-HMAC TAG-----\" >> ciphertext.pem")

# Remove auxiliary files
os.system("rm eph* *.bin ")
