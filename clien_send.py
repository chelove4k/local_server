import socket
import time

while True:
    message = input('>> ')
    message = message.replace('\\n', '')
    if not message:
        continue

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    HOST = local_ip
    PORT = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    try:
        s.sendall(b's')
        
        logs = s.recv(1024*10)
        # print(logs.decode())
        
        s.sendall(message.encode())
        
        data = s.recv(1024)
        print(data)
        
        s.close()
    except Exception as e: print(e)
    
    time.sleep(3)