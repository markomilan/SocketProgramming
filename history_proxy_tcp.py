from random import randint
from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR,timeout
import select, sys, time,struct, random, binascii, zlib, hashlib, json

# Create a TCP/IP socket
proxy_tcp = socket(AF_INET,SOCK_STREAM)
# Create a UDP/IP socket
proxy_udp = socket(AF_INET,SOCK_DGRAM)
proxy_udp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind the socket to the port
client_server_addr = ('localhost', 10001)
server_addr = ('localhost', 10000)

proxy_tcp.bind(client_server_addr)

# Listen for incoming connections by tcp
n = 3
proxy_tcp.listen(n)

# Variables

lotto_server = []
end = False
actMoney = 0
inputs = [proxy_tcp]
datas = {}

# The endings  
def sendEnd(sock):
    inputs.remove(sock)
    sock.close()
    proxy_udp.close()
    
# Functions    
def savetoJson(drawn_lotto,send_lotto,win):
    datas["lottos"] = []
    
    data = {"drawn_lotto" : drawn_lotto,
    "send_lotto" : send_lotto,
    "win" : win}
    
    datas["lottos"].append(data)
    print(datas)
    with open('data.json', 'w+') as outfile:
        json.dump(datas, outfile)
     

# Connections handling

while True:
    try:
        timeout = 1
        r, w, e = select.select(inputs,inputs,inputs,timeout)
        if not (r or w or e):
            continue
        for sock in r:
            if sock is proxy_tcp:
                print("Client is arrived")
                client, client_addr = sock.accept()
                inputs.append(client)
            else:
                data = sock.recv(5000)
                if data:
                    if end:
                        sendEnd(sock)
                    else:                       
                        unpacked_data = str(data, "utf-8")
                        proxy_udp.sendto(unpacked_data.encode(),server_addr)
                        data, _ = proxy_udp.recvfrom(1000)
                        if data:
                            answer = str(data, "utf-8")
                            #savetoJson(answer[0], unpacked_data[0], answer[0])
                            print(answer)
                            
                            packer = struct.Struct('I')
                            p_answer = packer.pack(int(answer))
                            sock.send(p_answer)
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
        proxy_udp.close()
        inputs = []
        
proxy_udp.close()