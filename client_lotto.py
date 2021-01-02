from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from random import randint
from sys import argv, exit
import sys, time, select, struct, zlib, binascii, hashlib, json

# Create a TCP/IP socket
#client = socket(AF_INET, SOCK_STREAM)

# Create a UDP socket
client = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to the port by tcp
#hostname = sys.argv[1]
#port = int(sys.argv[2])
#server_addr = (hostname,port)
server_addr = ('localhost',10000)
server_proxy_addr = ('localhost',10001)
#client.connect(server_addr)
#client.connect(server_proxy_addr)

# Variables
lotto_client = []
end = False
money = 0

# Functions    
def randLottoNumbers():
    while(len(lotto_client) != 5):
        num = randint(1,20)
        if num not in lotto_client:
            lotto_client.append(num)
    getMoney()
        
def getMoney():
    global money
    money = randint(100,1001)
    
def crc_maker(data):
    crc = 0
    crc = zlib.crc32(data.encode("utf-8"),crc)
    return str(crc)
    
def md5_maker(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return str(m.digest())
    
def input_LottoNumbers():
    global money
    while(len(lotto_client) != 5):
        num = input("Enter your tipp: ")
        if num not in lotto_client:
            lotto_client.append(int(num))
    money = int(input("Enter your bet: "))

def arg_LottoNumbers():
    global money
    arg = argv[1].split(',')
    money = int(argv[2])
    for i in arg:
        lotto_client.append(int(i))
   
def json_LottoNumbers():
    global money
    global lotto_client
    with open("data.json") as f:
        json_data = json.load(f)
    lotto_client = json_data["lotto"]
    money = json_data["money"]
    
def struct_sending():
    global money
    values = lotto_client, money
    print(lotto_client)
    #Struct(5*"I")
    p_tip = struct.Struct('5I I').pack(*(values[0]),values[1])
    #client.sendall(p_tip)
    #client.sendto(p_tip, server_addr)
    #client.sendto(p_tip, proxy_addr)
    
def byte_sending():
    global money
    b_lotto = str(lotto_clinet)
    b_lotto = b_lotto[1:-1]
    b_lotto = s_lotto.replace(", ",":")
    b_lotto = s_lotto + ":" + str(money)
    b = str((bytearray(b_lotto,"utf-8"))).encode()
    print(b)
    client.sendall(b)
    #client.sendto(b, server_addr)
    #client.sendto(b, proxy_addr)
    
def crc_sending():
    global money
    values = lotto_client, money
    print(lotto_client)
    p_tip = (str(values[0])[1:-1] + "," + str(values[1]) + "," +
        crc_maker(str(values[0])[1:-1] + "," + str(values[1]) + ",")).encode()
    #client.sendall(p_tip)
    #client.sendto(p_tip, server_addr)
    client.sendto(p_tip, server_proxy_addr)
 
def md5_sending():
    global money
    values = lotto_client, money
    print(lotto_client)
    p_tip = (str(values[0])[1:-1] + "," + str(values[1]) + "," +
        md5_maker(str(values[0])[1:-1] + "," + str(values[1]) + ",")).encode()
    #client.sendall(p_tip)
    #client.sendto(p_tip, server_addr)
    #client.sendto(p_tip, proxy_addr)

def use_tcp_recive():
    data = client.recv(8000)
    #data = client.recv(8000, socket.MSG_WAITALL)
    unpacked_data = struct.Struct('I').unpack(data)
    answer = unpacked_data
    print(answer[0]) 
    
def use_udp_revice():
    data = client.recvfrom(1000)
    answer = data[0].decode()
    print(answer)
    
# Connections handling
while not end:

    randLottoNumbers()
    #json_LottoNumbers()
    #arg_LottoNumbers()
    #input_LottoNumbers()
    
    #struct_sending()
    crc_sending()
    #md5_sending()
    #byte_sending()
    
    #use_tcp_recive()
    use_udp_revice()
    
    end = True
    
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nExit")
        sys.exit()
        
client.close()