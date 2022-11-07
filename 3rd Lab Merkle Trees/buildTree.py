import os

nodes_path = "./nodes/"


def createLayer(layerIndex, nFiles):
    counter = 0
    for j in range(0, nFiles, 2):
        if j == nFiles - 1 and nFiles % 2 == 1:
            os.system("cat node.pre " + nodes_path + "node" + str(layerIndex) + "." + str(j)
                      + " | openssl dgst -sha1 -binary | xxd -p > " + nodes_path + "node" + str(layerIndex + 1) + "."
                      + str(counter))
        else:
            os.system("cat node.pre " + nodes_path + "node" + str(layerIndex) + "." + str(
                j) + " " + nodes_path + "node" + str(layerIndex) + "."
                      + str(j + 1) + " | openssl dgst -sha1 -binary | xxd -p > " + nodes_path + "node" + str(
                layerIndex + 1)
                      + "." + str(counter))

        os.system("echo -n '" + str(layerIndex + 1) + ":" + str(counter) + ":' >> temp.txt")
        os.system("cat " + nodes_path + "node" + str(layerIndex + 1) + "." + str(counter) + " >> temp.txt")
        counter = counter + 1


os.system("echo -n '\x3C\x3C\x3C\x3C' > doc.pre")  # Creates the header for a document
os.system("echo -n '\xF5\xF5\xF5\xF5' > node.pre")  # Creates the header for a node
os.system("touch temp.txt")

docs_path = "./docs/"
docs_files = os.listdir(docs_path)

n = len(docs_files)  # Number of files in the "docs" directory

for i in range(n):
    os.system("cat doc.pre " + docs_path + docs_files[
        i] + " | openssl dgst -sha1 -binary | xxd -p > " + nodes_path + "node0." + str(i))
    os.system("echo -n '" + str(0) + ":" + str(i) + ":' >> temp.txt")
    os.system("cat " + nodes_path + "node" + str(0) + "." + str(i) + " >> temp.txt")

layer = 0
num_hashes = n
while num_hashes > 1:  # Determine if it is necessary to create another layer or the root is reached
    createLayer(layer, num_hashes)
    layer = layer + 1

    if num_hashes % 2 == 1:
        num_hashes = int(num_hashes / 2) + 1
    else:
        num_hashes = int(num_hashes / 2)

root_hash = os.popen("cat " + nodes_path + "node" + str(layer) + ".0").read()
public_info = "MerkleTree:sha1:3C3C3C3C:F5F5F5F5:" + str(n) + ":" + str(layer + 1) + ":" + root_hash

os.system("echo -n '" + public_info + "' > hash_tree.txt")
os.system("cat temp.txt >> hash_tree.txt")  # Appends the private info of the nodes to the hash tree file
os.system("rm temp.txt")
