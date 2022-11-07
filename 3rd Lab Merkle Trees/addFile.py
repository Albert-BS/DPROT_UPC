import os


def createLayer(layerIndex, nFiles):
    counter = 0
    for j in range(0, nFiles, 2):
        if j == nFiles - 1 and nFiles % 2 == 1:
            os.system("cat node.pre node" + str(layerIndex) + "." + str(j)
                      + " | openssl dgst -sha1 -binary | xxd -p > ./nodes/node" + str(layerIndex + 1) + "."
                      + str(counter))
        else:
            os.system("cat node.pre node" + str(layerIndex) + "." + str(j) + " node" + str(layerIndex) + "."
                      + str(j + 1) + " | openssl dgst -sha1 -binary | xxd -p > ./nodes/node" + str(layerIndex + 1)
                      + "." + str(counter))

        os.system("echo -n '" + str(layerIndex + 1) + ":" + str(counter) + ":' >> temp.txt")
        os.system("cat node" + str(layerIndex + 1) + "." + str(counter) + " >> temp.txt")
        counter = counter + 1


doc_path = input("Introduce the full path of the file you want to add:")

f = open("hash_tree.txt", "r")
public_info = f.readline()
info = public_info.rsplit(":")  # Getting public info of the hash tree to modify
num_hashes = int(info[-2])  # Getting the number of nodes of the hash tree

info_nodes = ""
for i in range(num_hashes):  # Reads the private info of the hash tree
    info_nodes = info_nodes + f.readline()
f.close()
os.system("cat doc.pre " + doc_path + " | openssl dgst -sha1 -binary | xxd -p > node0." + str(
    num_hashes))  # Computes the hash of the new node

f = open("temp.txt", "a")
f.write(info_nodes)
f.close()
os.system("echo -n '" + str(0) + ":" + str(
    num_hashes) + ":' >> temp.txt")  # Adding the new node to the private part of the hash tree
os.system("cat node" + str(0) + "." + str(num_hashes) + " >> temp.txt")
num_hashes = num_hashes + 1
old_nodes = num_hashes

layer = 0
while num_hashes > 1:  # Determine if it is necessary to create another layer or the root is reached
    createLayer(layer, num_hashes)
    layer = layer + 1

    if num_hashes % 2 == 1:

        num_hashes = int(num_hashes / 2) + 1
    else:

        num_hashes = int(num_hashes / 2)

root_hash = os.popen("cat node" + str(layer) + ".0").read()
public_info = "MerkleTree:sha1:353535353535:e8e8e8e8e8e8:" + str(old_nodes) + ":" + str(
    layer + 1) + ":" + root_hash  # Recomputing the public info of the hash tree

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt")  # Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")
