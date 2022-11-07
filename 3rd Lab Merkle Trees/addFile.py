import os

nodes_path = "./nodes/"

doc_path = input("Introduce the full path of the file you want to add:")

f = open("hash_tree.txt", "r")
public_info = f.readline()  # doc.pre + node.pre + root hash
info = public_info.rsplit(":")  # Getting public info of the hash tree to modify
num_hashes = int(info[-3])  # Getting the number of files composing the Merkle tree

info_nodes = ""
for i in range(num_hashes):  # Reads the private info of the hash tree
    info_nodes = info_nodes + f.readline()
f.close()
os.system("cat doc.pre " + doc_path + " | openssl dgst -sha1 -binary | xxd -p > " + nodes_path + "node0." + str(
    num_hashes))  # Computes the hash of the new node

f = open("temp.txt", "a")
f.write(info_nodes)  # Write previous files: 0:0 to 0:num_hashes-1
f.close()
os.system("echo -n '" + str(0) + ":" + str(num_hashes) + ":' >> temp.txt")  # Adding the new node
os.system("cat " + nodes_path + "node" + str(0) + "." + str(num_hashes) + " >> temp.txt")

i = 0
j = num_hashes
while j > 0:
    i = i + 1
    odd = j % 2
    j = int(j/2)
    if odd == 1:
        os.system("cat node.pre " + nodes_path + "node" + str(i-1) + "." + str(2 * j) + " "
                  + nodes_path + "node" + str(i-1) + "." + str(2 * j + 1) + " | openssl dgst -sha1 -binary | xxd -p > "
                  + nodes_path + "node" + str(i) + "." + str(j))
    else:
        os.system("cat node.pre " + nodes_path + "node" + str(i-1) + "." + str(2 * j)
                  + " | openssl dgst -sha1 -binary | xxd -p > " + nodes_path + "node" + str(i) + "." + str(j))
    os.system("echo -n '" + str(i) + "." + str(j) + ":' >> temp.txt")
    os.system("cat " + nodes_path + "node" + str(i) + "." + str(j) + " >> temp.txt")

n = num_hashes
layer = 0
while n > 1:
    counter = 0
    for k in range(0, n, 2):
        os.system("echo -n '" + str(layer + 1) + ":" + str(counter) + ":' >> temp.txt")
        os.system("cat " + nodes_path + "node" + str(layer+1) + "." + str(counter) + " >> temp.txt")
        counter = counter + 1
    layer = layer + 1
    if n % 2 == 1:
        n = int(n/2) + 1
    else:
        n = int(n/2)

root_hash = os.popen("cat " + nodes_path + "node" + str(i) + ".0").read()
public_info = "MerkleTree:sha1:3C3C3C3C:F5F5F5F5:" + str(num_hashes) + ":" + str(
    i + 1) + ":" + root_hash  # Recomputing the public info of the hash tree

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt")  # Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")
