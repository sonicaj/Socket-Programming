import socket
from time import sleep

if __name__ == '__main__':
    s = socket.socket()

    host = socket.gethostname()
    port = 6188

    s.connect((host,port))
    print('Connected with server')
    s.sendall(b'3')
    sleep(2)
    s.sendall(b'2')
    data = s.recv(1024)
    data = repr(data)
    print('Connection with client established ' if data[2:len(data)-1] == 'Connection established' else ' ')
    if data[2:len(data) - 1] == 'Connection established':
        sleep(5)
    checkConnection = True
    while checkConnection:
        if data[2:len(data)-1] == 'Requested client has not connected yet, Please wait':
            print(data[2:len(data) - 1])
            data = s.recv(1024)
            data = repr(data)
            print('Connection with client established ' if data[2:len(data) - 1] == 'Connection established' else ' ')
            continue
        elif data[2:len(data)-1] == 'Client rejected connection':
            print('Requested client rejected connection')
            break
        else:
            checkSend,checkRecieve = True,True
            print('Waiting for Client to respond')
            while checkRecieve:
                data = s.recv(1024)
                data = repr(data)
                if data[2:5] == 'end':print('Connection terminated'); checkConnection,checkSend = False,False;break
                print('Client has a message for you  : \n', data[2:len(data) - 1])
                if data[len(data) - 2:len(data)-1] == '.':
                    checkRecieve = False
            while checkSend :
                data = str(input('What do you want to say to Client ( to end connection type end ) : '))
                if data[len(data) - 1:] == '.':checkSend = False
                data = bytes(data, 'utf8')
                s.sendall(data)
                data = repr(data)
                if data[2:5] == 'end': print('Connection terminated');checkConnection = False;break
    s.close()
