import socket
from time import sleep

if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 6188
    s.connect((host,port))
    print('Connected with server')

    s.sendall(b'2')
    sleep(2)
    s.sendall(b'3')
    data = s.recv(1024)
    data = repr(data)
    print('Connection with client established ' if data[2:len(data) - 1] == 'Connection established' else ' ')
    while True:
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
            data = str(input('Please input the data you want to send to client ( to end connection type end ) : '))
            data = bytes(data, 'utf8')
            s.sendall(data)
            print('Waiting for Client to respond')
            data = s.recv(1024)
            data = repr(data)
            if data[2:5] == 'end': print('Connection terminated');break
            print('Client has a message for you  : \n', data[2:len(data) - 1])
    s.close()