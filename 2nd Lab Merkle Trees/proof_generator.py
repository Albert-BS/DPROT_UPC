import os
import math

docs_path = "./docs/"
text = open('hash_tree.txt', 'r')
lines = text.readlines()

n = int(lines[0].split(':')[-2])  # Number of layers
nDocs = int(lines[0].split(':')[-3])  # Number of documents

j = int(input("Position of the document:"))

proof = open('proof.txt', 'w')
proof.write(lines[0])
proof.close()

for i in range(n - 1):
    if (j % 2) == 0:
        if (j + 1) < nDocs:
            os.system("echo -n '" + str(i) + ":" + str(j + 1) + ":' >> proof.txt")
            os.system("cat nodes/node" + str(i) + "." + str(j + 1) + " >> proof.txt")
        else:
            os.system("echo -n '" + str(i) + ":" + str(j + 1) + ":\n' >> proof.txt")
    else:
        os.system("echo -n '" + str(i) + ":" + str(j - 1) + ":' >> proof.txt")
        os.system("cat nodes/node" + str(i) + "." + str(j - 1) + " >> proof.txt")

    j = math.trunc(j / 2)
    i = i + 1
    nDocs = math.trunc(nDocs / 2 + nDocs % 2)
