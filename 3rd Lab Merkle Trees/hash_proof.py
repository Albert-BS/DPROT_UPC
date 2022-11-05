import math
import os


os.system("echo -n '\x35\x35\x35\x35\x35\x35' > doc.pre")

file_path = []
file_path.append(input("Type the path of the node that you want to verify:"))
os.system("cat doc.pre " + file_path + " | openssl dgst -sha1 -binary | xxd -p > node0" )

i=0
j=7
N=4
nodes=[None]*(N-1)
for k in range(N-1):
    if((j+2)%2 ==0 ):
        nodes[k]=str(i)+":"+str(j+1)
    else:
        nodes[k]=str(i)+":"+str(j-1)
    i=i+1
    j=math.trunc(j/2)

print(nodes)

## TEST
i=0
text=open('info.txt','r')
for line in text.readlines(text):
    if(i==N-1):
        break
    if nodes[i] in line:
        next_node=line.split(":")[-1]
        os.system("cat node0 next_node | openssl dgst -sha1 -binary > node"+str(i+1))
        i=i+1

