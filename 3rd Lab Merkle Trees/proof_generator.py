import math
import os
import math

docs_path = "./docs/"
text=open('hash_tree.txt','r')
lines=text.readlines()

N=int(lines[0].split(':')[-2]) ## Number of layers
i=0 
j=int(input("Position of the document:"))

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
