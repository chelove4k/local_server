import socket
 
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    HOST = local_ip
    return local_ip

if __name__ == '__main__':
    local_ip = get_local_ip()
    
    print(local_ip)