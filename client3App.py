import socket
from time import sleep

if __name__ == '__main__':

    print('hello')
    s = socket.socket()

    host = socket.gethostname()
    port = 6188

    s.connect((host,port))
    print('Connection with client successfully created')

    s.sendall(b'3')
    sleep(2)
    s.sendall(b'2')
    data = s.recv(1024)
    data = repr(data)
    print('Connection with client established ' if data[2:len(data)-1] == 'Connection established' else ' ')
    if data[2:len(data) - 1] == 'Connection established':
        sleep(5)
    while True:
        if data[2:len(data)-1] == 'Requested client has not connected yet, Please wait':
            print(data[2:len(data) - 1])
            data = s.recv(1024)
            data = repr(data)
            continue
        elif data[2:len(data)-1] == 'Client rejected connection':
            print('Requested client rejected connection')
            break
        else:
            data = s.recv(1024)
            data = repr(data)
            if data[2:5] == 'end':print('Connection terminated'); break
            print('Client has a message for you  : \n', data[2:len(data) - 1])
            data = str(input('Please reply what you want to say to Client ( to end connection type end ) : '))
            data = bytes(data, 'utf8')
            s.sendall(data)
            print('Waiting for Client to respond')
    s.close()