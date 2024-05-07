import socket
import json
import time

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
HOST = local_ip
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
logtime = 100

def read(conn):
        try:
                print('mode = r')
                logs = ''
                k = 0
                datalist = json.load(open('logs.json'))['logs']
                if len(datalist) > logtime:
                        datalist = datalist[-1*logtime:]
                for i in datalist:
                        logs += str(k) + ' : ' + str(i) + '\n'
                        k += 1

                conn.sendall(logs.encode())

                conn.close()
        except Exception as e: print(e)

def send(conn):
        try:
                print('mode = s')

                logs = ''
                k = 0
                datalist = json.load(open('logs.json'))['logs']
                if len(datalist) > logtime:
                        datalist = datalist[-1*logtime:]
                for i in datalist:
                        logs += str(k) + ' : ' + str(i) + '\n'
                        k += 1

                print('sending logs...')
                conn.sendall(logs.encode())

                print('recv user data...')
                data = conn.recv(1024).decode()
                print(f'data : {data}')

                print('saving logs to file')
                log_file = json.load(open('logs.json'))
                log_file['logs'].append(data)
                json.dump(log_file, open('logs.json', 'w'))

                print('closing connection!')
                conn.sendall(b'done!')
                conn.close()       
        except Exception as e: print(e)

def admin(conn):
        """
        команды:
        Максимальная длинна логов (для всех) *
        Удаление сообщения *
        Пауза *
        Выделеное сообщение *
        Отчистка логов
        
        Структура команды:
        
        команда значение
        """
        try:
                command = conn.recv(1024).decode()
                command = str(command)
                command = command.split(' ')

                if command[0] == 'logtime' and len(command) == 2 and int(command[1]) > 0:
                        global logtime
                        logtime = int(command[1])
                        print('logtime is changed to', logtime)
                        
                        conn.sendall(b'Done!')
                        conn.close()
                elif command[0] == 'delmessage' and len(command) == 2 and int(command[1]) > 0:
                        
                        logs = json.load(open('logs.json'))
                        logs['logs'].pop(int(command[1]))
                        json.dump(logs, open('logs.json', 'w'))
                        conn.sendall(b'Done!')
                        conn.close()
                        
                elif command[0] == 'pause' and len(command) == 2 and int(command[1]) > 0:
                        
                        time.sleep(int(command[1]))
                        conn.sendall(b'Done!')
                        conn.close()
                        
                elif command[0] == 'sypermessage':
                        
                        log_file = json.load(open('logs.json'))
                        message = ''
                        for i in command[1:]:
                                message += i + ' '
                        log_file['logs'].append(str(f'\n===========\n{message}\n==========='))
                        json.dump(log_file, open('logs.json', 'w'))
                        conn.sendall(b'Done!')
                        conn.close()
                        
                else:
                        conn.sendall(b'Wrong command!')
                        conn.close()
                        
        except Exception as e: print(e)
        
        

def main():
        while True:
                try:
                        conn, addr = s.accept()
                        print(f'connected by {addr}')
                        mode = conn.recv(1) 
                        
                        if mode == b'r':
                                read(conn)
                        elif mode == b's':
                                send(conn)
                        elif mode == b'a':
                                admin(conn)
                        
                        
                except Exception as e: print(e)
          
          
if __name__ == '__main__':
        main()
    
    