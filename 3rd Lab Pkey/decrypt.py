import os

name = input("Introduce the name of the destinatary:")
filename = input("Introduce the ciphertext file name:")

if not os.path.isfile(name + "_pkey.pem"):
    print("Missing public key file")
    exit()

file = open(filename, "r")
ciphertext = file.read()
file.close()

pubKeyIndex = ciphertext.find("-----END PUBLIC KEY-----")
pubkey = ciphertext[:pubKeyIndex+24]
os.system("echo -n \"" + pubkey + "\" > ephpub.pem")

ivIndex = ciphertext.find("-----END AES-128-CBC IV-----")
iv = ciphertext[pubKeyIndex+56:ivIndex]
os.system("echo -n \"" + iv + "\" | openssl base64 -d -out iv.bin")

cipherIndex = ciphertext.find("-----END AES-128-CBC CIPHERTEXT-----")
cipher = ciphertext[ivIndex+68:cipherIndex]
os.system("echo -n \"" + cipher + "\" | openssl base64 -d -out ciphertext.bin")

tagIndex = ciphertext.find("-----END SHA256-HMAC TAG-----")
tag = ciphertext[cipherIndex+69:tagIndex]
os.system("echo -n \"" + tag + "\" | openssl base64 -d -out tag.bin")

os.system("openssl pkeyutl -inkey " + name + "_pkey.pem -peerkey ephpub.pem -derive -out common.bin")

os.system("cat common.bin | openssl dgst -sha256 -binary | head -c 16 > k1.bin")
os.system("cat common.bin | openssl dgst -sha256 -binary | tail -c 16 > k2.bin")

os.system("cat iv.bin ciphertext.bin | openssl dgst -sha256 -mac hmac -macopt hexkey:`cat k2.bin | xxd -p` -binary > decryptedTag.bin")

if os.popen("cat tag.bin | openssl base64").read() == os.popen("cat decryptedTag.bin | openssl base64").read():
    os.system(
        "openssl enc -aes-128-cbc -d -in ciphertext.bin -iv `cat iv.bin | xxd -p` -K `cat k1.bin | xxd -p` -out decrypted.txt")

else:
    print("Wrong TAG! Specify the expected recevier")

os.system("rm eph* *.bin")