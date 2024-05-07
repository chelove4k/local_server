import socket
import os
import time

local_ip = input('ip >>')
while True:
    hostname = socket.gethostname()
    # local_ip = socket.gethostbyname(hostname)
    HOST = local_ip
    PORT = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    try:
        s.sendall(b'r')
        
        data = s.recv(1024*10).decode()
        print(data)
        
        s.close()
        
    except Exception as e: print(e)
    
    time.sleep(3)
    os.system('cls')
