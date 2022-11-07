import math
import os
import time
import math



file_path = []
file_path.append(input("Type the path of the node that you want to verify:"))
print(file_path[0])
n= input("Type the number of documents the hash tree contains:")  
N = math.trunc(math.log(int(n),2))+2
print("Number of layers: ",N)

i=int(file_path[0][4])
j=int(file_path[0][6])

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
text=open('hash_tree.txt','r')
proof=open('proof.txt','w')
lines=text.readlines()
for line in lines:
    if("MerkleTree" in line):
        end_node=line.split(':')[-1]
    if(i==N-1):
        break
    if nodes[i] in line:
        proof.write(line)
        i=i+1
        
proof.close()


## TEST

i=0
proof=open('proof.txt','r')
lines=proof.readlines()
for line in lines:
    next_node=((line.split(":"))[-1]).split('\n')[0]
    print('Next node: ',next_node)
    command="echo '"+next_node+"' >next_node"+str(i)
    os.system(command)

    if(i==0):
        if((line.split(":")[1])>(file_path[0]).split('.')[-1]):
            nodes_c= file_path[0]+" next_node"+str(i)
        else:
            nodes_c= "next_node"+str(i)+" "+file_path[0]

        #print(nodes_c)

        os.popen("cat node.pre "+nodes_c+" | openssl dgst -sha1 -binary | xxd -p > node"+str(i))
        time.sleep(1)
        print('node0: ',os.popen('cat node'+str(i)).read())
    else:
        if((line.split(":")[1])>aux):
            nodes_c= "node"+str(i-1)+" next_node"+str(i)
        else:
            nodes_c= "next_node"+str(i)+" node"+str(i-1)

        print(nodes_c)
        os.system("cat node.pre "+nodes_c+" | openssl dgst -sha1 -binary | xxd -p > node"+str(i))
        print('node'+str(i)+': ',os.popen('cat node'+str(i)).read())

    i=i+1
    aux=(line.split(":")[1])


last_node=os.popen('cat node'+str(i-1)).read()

if(last_node==end_node):
    print("OK")