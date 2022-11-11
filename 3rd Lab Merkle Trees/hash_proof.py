import math
import os
import math

docs_path = "./docs/"
text=open('hash_tree.txt','r')
lines=text.readlines()

N=int(lines[0].split(':')[-2]) ## Number of layers
i=0 
j=int(input("Position of the document:"))
print(N,j)

os.system( "cat doc.pre "+docs_path+"doc"+str(j)+" | openssl dgst -sha1 -binary | xxd -p > node0."+str(j))

nodes=[None]*(N-1)
for k in range(N-1):
    if((j+2)%2 ==0 ):
        nodes[k]=str(i)+":"+str(j+1)
    else:
        nodes[k]=str(i)+":"+str(j-1)
    i=i+1
    j=math.trunc(j/2)

print("List of nodes that we need to verify the proof: ",nodes)

i=0

proof=open('proof.txt','w')
proof.write(lines[0])
for line in lines:
    if(i==N-1):
        break
    if nodes[i] in line:
        proof.write(line)
        i=i+1
        
proof.close()


## TEST

i=0
j=int(input("Position of the document:"))
proof=open('proof.txt','r')
lines=proof.readlines()
for line in lines:
    if("MerkleTree" in line):
        end_node=line.split(':')[-1]
    else:
        next_node=((line.split(":"))[-1]).split('\n')[0]
        print('Next node: ',next_node)

        command="echo '"+next_node+"' >node"+line.split(":")[0]+"."+line.split(":")[1]
        print(command)
        os.system(command)

        if((int(line.split(":")[1]))>j):
            nodes_c= "node"+str(i)+"."+str(j)+" node"+line.split(":")[0]+"."+line.split(":")[1]
        else:
            nodes_c= "node"+line.split(":")[0]+"."+line.split(":")[1]+" node"+str(i)+"."+str(j)
            

        print(nodes_c)

        j=math.trunc(j/2)
        print(j)
        i=i+1
        os.popen("cat node.pre "+nodes_c+" | openssl dgst -sha1 -binary | xxd -p > node"+str(i)+"."+str(j))
        print('>> node'+str(i)+"."+str(j),os.popen('cat node'+str(i)+"."+str(j)).read())


last_node=os.popen('cat node'+str(i)+"."+str(j)).read()

if(last_node==end_node):
    print("OK")