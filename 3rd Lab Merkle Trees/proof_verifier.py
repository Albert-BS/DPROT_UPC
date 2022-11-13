import os
import math

docs_path = "./docs/"

i = 0
j = int(input("Position of the document:"))

proof = open('proof.txt', 'r')

public_info = proof.readline()
info = public_info.split(':')

alg = info[-6]
end_node = info[-1]

os.system(
    "cat doc.pre " + docs_path + "doc" + str(j) + ".dat | openssl dgst -" + alg + " -binary | xxd -p > aux_hash.txt")

lines = proof.readlines()

for line in lines:
    os.system(
        "cp aux_hash.txt aux_hash1.txt")  # We need to create a copy since in the last command we need a secondary file to compute the new hash or it will try to open two times the same file, one for reading and one for writing
    next_node = ((line.split(":"))[-1]).split('\n')[0]
    os.system("echo '" + next_node + "' > next_node.txt")

    # Constructing the nodes command in the good order

    if line[4] == "\n":  # Check if the node exists or not
        nodes_c = "aux_hash1.txt"
    else:
        if (int(line.split(":")[1])) > j:
            nodes_c = "aux_hash1.txt next_node.txt"
        else:
            nodes_c = "next_node.txt aux_hash1.txt"

    # indexes of the following node

    j = math.trunc(j / 2)
    i = i + 1

    # Generating the following node

    os.system("cat node.pre " + nodes_c + " | openssl dgst -" + alg + " -binary | xxd -p > aux_hash.txt")

# Verify if the node calculated with the proof.txt file is the same that the root real has value

last_node = os.popen("cat aux_hash.txt").read()

if last_node == end_node:
    print("OK, proof verified")
else:
    print("Wrong, not verified")

os.system("rm aux_hash.txt aux_hash1.txt next_node.txt")