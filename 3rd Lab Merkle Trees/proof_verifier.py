import math
import os
import math
import time

## TEST

docs_path = "./docs/"

i=0
j=int(input("Position of the document:"))
os.system( "cat doc.pre "+docs_path+"doc"+str(j)+" | openssl dgst -sha1 -binary | xxd -p > node0."+str(j))

proof=open('proof.txt','r')
lines=proof.readlines()
for line in lines:
    if("MerkleTree" in line):
        end_node=line.split(':')[-1] ## Root real hash value
    else:
        next_node=((line.split(":"))[-1]).split('\n')[0]
        print('Next node: ',next_node)

        command="echo '"+next_node+"' >node"+line.split(":")[0]+"."+line.split(":")[1]
        #print(command)
        os.system(command)

        ## Constructing the nodes command in the good order

        if((int(line.split(":")[1]))>j):
            nodes_c= "node"+str(i)+"."+str(j)+" node"+line.split(":")[0]+"."+line.split(":")[1]
        else:
            nodes_c= "node"+line.split(":")[0]+"."+line.split(":")[1]+" node"+str(i)+"."+str(j)
            

        print("Nodes used to calculate the following command: ",nodes_c)
        
        ## indexes of the following node

        j=math.trunc(j/2)
        i=i+1

        ## Generating the following node

        os.popen("cat node.pre "+nodes_c+" | openssl dgst -sha1 -binary | xxd -p > node"+str(i)+"."+str(j))
        time.sleep(2)
        print('>> node'+str(i)+"."+str(j),os.popen('cat node'+str(i)+"."+str(j)).read())


## Verify if the node calculated with the proof.txt file is the same that the root real has value

last_node=os.popen('cat node'+str(i)+"."+str(j)).read()

if(last_node==end_node):
    print("OK, proof verified")