import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = ''
    port = 6188

    s.connect((host,port))
    print('Client 2 connected with server ')
    while True:
        data = s.recv(1024)
        data = repr(data)
        if data[2:5] == 'end' : break
        print('Client 1 has a message for you  : \n', data[2:len(data)-1])
        data = str(input('Please reply what you want to say to Client 1 ( to end connection type end ) : '))
        data = bytes(data,'utf8')
        s.sendall(data)
    s.close()
