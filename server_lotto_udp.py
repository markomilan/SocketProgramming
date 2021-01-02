from random import randint
from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR,timeout
import select, sys, struct, time,random, binascii, zlib, hashlib, json

# Create a UDP socket
server = socket(AF_INET,SOCK_DGRAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind the socket to the port
server_addr = ('localhost', 10000)
server.bind(server_addr)
server.settimeout(1.0)
# Variables

lotto_server = []
end = True
actMoney = 0

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

while end:
    try:
        data, client_addr = server.recvfrom(1000)
        if data:
            #packer = struct.Struct('5I I')
            #unpacked_data = packer.unpack(data)
            
            unpacked_data = str(data, "utf-8").split(",")
            print(unpacked_data)
            lotto_client = [unpacked_data[0],unpacked_data[1],
            unpacked_data[2],unpacked_data[3],unpacked_data[4]]
            
            answer = getPrize(lotto_client, unpacked_data[5])
            #answer = getPrize(lotto_client, unpacked_data[5]),lotto_server
            server.sendto(str(answer).encode(),client_addr)
        else:
            print("Client quited")
            server.close()

    except timeout:
        pass
    except KeyboardInterrupt:
        print("Close the system")
        pass
server.close()