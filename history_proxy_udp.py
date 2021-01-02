from random import randint
from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR,timeout
import select, sys, time,struct, random, binascii, zlib, hashlib, json

# Create a UDP socket
proxy_udp = socket(AF_INET,SOCK_DGRAM)
proxy_udp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Create a TCP/IP socket
proxy_tcp = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
client_server_addr = ('localhost', 10001)
server_addr = ('localhost', 10000)

proxy_udp.bind(client_server_addr)
proxy_udp.settimeout(1.0)

proxy_tcp.connect(server_addr)
# Variables

# Connections handling

while True:
    try:
        data, client_addr = proxy_udp.recvfrom(1000)
        if data:
            #packer = struct.Struct('5I I')
            #unpacked_data = packer.unpack(data)
            
            unpacked_data = str(data, "utf-8").split(",")
            print(unpacked_data)
            proxy_tcp.sendall(data)
            
            data = proxy_tcp.recv(5000)
            if data:
                unpacked_data = struct.Struct('I').unpack(data)
                print(unpacked_data)
                
                proxy_udp.sendto(str(unpacked_data).encode(),client_addr)
            else:
                proxy_tcp.close()
        else:
            print("Client quited")
            proxy_udp.close()

    except timeout:
        pass
    except KeyboardInterrupt:
        print("Close the system")
        proxy_udp.close()
        proxy_tcp.close()
        
proxy_udp.close()
proxy_tcp.close()