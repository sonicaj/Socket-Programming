import socket
import sys
from _thread import *
import threading
global conn1,conn2

def communicate(host,port):
    global conn1,conn2
    print('Communicate func executing')
    while True:
        data = conn1.recv(1024)
        conn2.sendall(data)
        data = repr(data)
        if data[2:5] == 'end':
            print('client 1 ending the connection')
            conn1.sendall(b'end')
            break
        data = conn2.recv(1024)
        conn1.sendall(data)
        data = repr(data)
        if data[2:5] == 'end':
            print('client 2 ending the connection')
            conn2.sendall(b'end')
            break
    conn1.close()
    conn2.close()


if __name__ =='__main__':
    global conn1,conn2
    host = ''
    port = 6188
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created successfully')

    try:
        s.bind((host,port))
    except socket.error as msg:
        print('Couldnt bind socket, error occurred with error code : ', msg[1])
        sys.exit(0)
    print('Socket binded successfully')

    s.listen(2)
    print('Socket listening now')
    i = 0
    while True:
        if i == 2 : break
        if i == 0:
            conn1, addr = s.accept()
        else:
            conn2,addr = s.accept()
        i += 1
        if i == 2 :
            t = threading.Thread(None,communicate,'thread1',(host,port),None)
            t.start()
    t.join()
    s.close()
