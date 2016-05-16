import socket
from time import sleep

if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 6188
    s.connect((host,port))
    print('Connected with server')

    s.sendall(b'0')
    sleep(2)
    s.sendall(b'1')
    data = s.recv(1024)
    data = repr(data)
    print('Connection with client established ' if data[2:len(data) - 1] == 'Connection established' else ' ')
    checkConnection = True
    while checkConnection:
        if data[2:len(data)-1] == 'Requested client has not connected yet, Please wait':
            print('Requested client has not connected yet, Please wait')
            data = s.recv(1024)
            data = repr(data)
            print('Connection with client established ' if data[2:len(data) - 1] == 'Connection established' else ' ')
            continue
        elif data[2:len(data) - 1] == 'Client rejected connection':
            print('Requested client rejected connection')
            break
        else:
            checkSend,checkRecieve = True,True
            while checkSend:
                data = str(input('Please input the data you want to send to client ( to end connection type end ) : '))
                if data[len(data)-1:] == '.':
                    checkSend = False
                data = bytes(data, 'utf8')
                s.sendall(data)
                data = repr(data)
                if data[2:5] == 'end': print('Connection terminated');checkConnection, checkRecieve = False, False;break
            print('Waiting for cient to respond' if checkRecieve else '')
            while checkRecieve:
                data = s.recv(1024)
                data = repr(data)
                if data[len(data)-2:len(data)-1] == '.':
                    checkRecieve = False
                if data[2:5] == 'end': print('Connection terminated');checkConnection, checkRecieve = False, False;break
                print('Client has a message for you  : \n', data[2:len(data) - 1])
    s.close()
