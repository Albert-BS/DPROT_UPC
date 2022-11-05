import os


def createLayer(layerIndex, nFiles):

    counter = 0
    for j in range(0, nFiles, 2):
        if j == nFiles - 1 and nFiles % 2 == 1:
            os.system(
                "cat node.pre node" + str(layerIndex) + "." + str(j) + " | openssl dgst -sha1 -binary | xxd -p > node" + str(
                    layerIndex + 1) + "." + str(counter))
        else:
            os.system("cat node.pre node" + str(layerIndex) + "." + str(j) + " node" + str(layerIndex) + "." + str(
                j + 1) + " | openssl dgst -sha1 -binary | xxd -p > node" + str(layerIndex + 1) + "." + str(counter))

        os.system("echo -n '" + str(layerIndex + 1) + ":" + str(counter) + ":' >> temp.txt")
        os.system("cat node" + str(layerIndex + 1) + "." + str(counter) + " >> temp.txt")
        counter = counter + 1


os.system("echo -n '\x35\x35\x35\x35\x35\x35' > doc.pre")  # Creates the header for a document
os.system("echo -n '\xe8\xe8\xe8\xe8\xe8\xe8' > node.pre")  # Creates the header for a node
os.system("touch temp.txt")

n = input(
    "Type the number of files the hash tree will contain:")  # Request the number of files the hash tree will contain
n = int(n)

file_path = []
for i in range(n):  # Request the path of each file and computes the hash
    file_path.append(input("Type the path of the file " + str(i + 1) + ":"))
    os.system("cat doc.pre " + file_path[i] + " | openssl dgst -sha1 -binary | xxd -p > node0." + str(i))
    os.system("echo -n '" + str(0) + ":" + str(i) + ":' >> temp.txt")
    os.system("cat node" + str(0) + "." + str(i) + " >> temp.txt")

layer = 0
num_hashes = n
while num_hashes > 1:  # Determine if it is necessary to create another layer or the root is reached
    createLayer(layer, num_hashes)
    layer = layer + 1

    if num_hashes % 2 == 1:

        num_hashes = int(num_hashes / 2) + 1
    else:

        num_hashes = int(num_hashes / 2)

root_hash = os.popen("cat node" + str(layer) + ".0").read()
public_info = "MerkleTree:sha1:353535353535:e8e8e8e8e8e8:" + str(n) + ":" + str(
    layer + 1) + ":" + root_hash  # Appends the root hash to the hash tree public info

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt")  # Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")