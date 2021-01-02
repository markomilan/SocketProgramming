from random import randint
from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR,timeout
import select, sys, struct, random, binascii, zlib, hashlib, json

# Create a TCP/IP socket
server = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
#hostname = sys.argv[1]
#port = int(sys.argv[2])
server_addr = ('localhost', 10000)
#server_addr = (hostname,port)
server.bind(server_addr)

# Listen for incoming connections by tcp
n = 3
server.listen(n)

# Variables

lotto_server = []
end = False
actMoney = 0
inputs = [server]

# The endings  
def sendEnd(sock):
    inputs.remove(sock)
    sock.close()
    
# Functions    
def randLottoNumbers():
    while(len(lotto_server) != 5):
        num = randint(1,20)
        if num not in lotto_server:
            lotto_server.append(num)
        
def getPrize(lotto_client, actMoney):
    
    correctNums = 0
    for i in lotto_server:
        for j in lotto_client:
            if i == int(j):
                correctNums += 1
    
    print(correctNums,"!")
    return int(actMoney) * correctNums
            
    

# Connections handling

randLottoNumbers()

while True:
    try:
        timeout = 1
        r, w, e = select.select(inputs,inputs,inputs,timeout)
        if not (r or w or e):
            continue
        for sock in r:
            if sock is server:
                print("Client is arrived")
                client, client_addr = sock.accept()
                inputs.append(client)
            else:
                data = sock.recv(5000)
                if data:
                    if end:
                        sendEnd(sock)
                    else:
                        #packer = struct.Struct('5I I')
                        #unpacked_data = packer.unpack(data)
                        #unpacked_data = list(packer.unpack(data))
                        
                        unpacked_data = str(data, "utf-8").split(",")
                        
                        lotto_client = [unpacked_data[0],unpacked_data[1],
                        unpacked_data[2],unpacked_data[3],unpacked_data[4]]
                        print(unpacked_data)
                        print(lotto_server)
                        
                        answer = getPrize(lotto_client, unpacked_data[5])
                        packer = struct.Struct('I')
                        p_answer = packer.pack(answer)
                        sock.sendall(p_answer)
                        
                        if end:
                            sendEnd(sock)

                else:
                    print(str(sock.getpeername()) + ' quited!')
                    inputs.remove(sock)
                    sock.close()
                    
    except KeyboardInterrupt:
        print("Close the system")
        for s in inputs:
            s.close()
        inputs = []
