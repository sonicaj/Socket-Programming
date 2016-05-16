import socket
import sys
from _thread import *
import threading

global conn
global addr

def connected(client1,client2):
    global conn,addr
    terminate = False
    while True:
        checkClient1 ,checkClient2 = True,True
        while checkClient1:
            data = conn[client1].recv(1024)
            conn[client2].sendall(data)
            data = repr(data)
            if data[len(data)-2:len(data)-1] == '.':
                checkClient1 = False
            if data[2:len(data)-1] == 'end':
                print('Client ',client1, ' ending the connection with Client ',client2)
                terminate = True
                break
        while checkClient2 and terminate == False:
            data = conn[client2].recv(1024)
            conn[client1].sendall(data)
            data = repr(data)
            if data[len(data)-2:len(data)-1] == '.':
                checkClient2 = False
            if data[2:len(data)-1] == 'end':
                print('Client ',client2,' Ending the connection with Client ',client1)
                terminate = True
                break
        if terminate == True : break
    conn[client1].close()
    conn[client2].close()


if __name__ == '__main__':
    global conn,addr
    conn = []
    addr = []
    reqConn = []
    arrivalQueue = dict()
    arrive = []
    t = []
    host = socket.gethostname()
    port = 6188

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket successfully created')

    try:
        s.bind((host,port))
    except socket.errno as msg:
        print('Couldnt bind socket, Error occured with error No : ' , msg[0])
        sys.exit(0)

    print('Socket successfully binded')

    s.listen(6)
    print('Socket listening')
    i = 0;tCount = 0
    while True:
        if i == 2 : break
        tempConn,tempAddr = s.accept()
        conn.append(tempConn)
        addr.append(tempAddr)
        data = conn[i].recv(1024)
        data = repr(data)
        data2 = conn[i].recv(1024)
        data2 = repr(data2)
        reqConn.append(int(data2[2:3]))
        id = int(data[2:3])
        arrivalQueue[id] = {'index': i,'wants':int(data2[2:3])}
        arrive.append(id)
        if arrivalQueue[id]['wants'] in arrive:
            if arrivalQueue[arrivalQueue[id]['wants']]['wants'] == id:
                conn[i].sendall(b'Connection established')
                conn[arrivalQueue[arrivalQueue[id]['wants']]['index']].sendall(b'Connection established')
                if id%2 == 0:
                    t.append(threading.Thread(None,connected,None,(i,arrivalQueue[arrivalQueue[id]['wants']]['index']),None))
                else:
                    t.append(threading.Thread(None, connected, None,(arrivalQueue[arrivalQueue[id]['wants']]['index'],i), None))
                t[tCount].start()
                tCount += 1
            else:
                conn[i].sendall(b'Client rejected connection')
                conn[i].close()
        else:
            conn[i].send(b'Requested client has not connected yet, Please wait')
        i += 1
    for i in range(tCount):
        t[i].join()
    print('All clients have exited, Server closing down')
    s.close()
