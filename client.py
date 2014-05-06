import socket

ServerAddress = ('109.186.103.151', 20020)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

s.sendto('\x01', ServerAddress)
while True:
    try:
        data1, addr = s.recvfrom(1)
        if data1 == '\x02':
            print('connection to server successful')
            break
    except socket.timeout:
        s.sendto('\x01', ServerAddress)
        print('attempting connection to server...')

while True:
    try:
        data2, addr = s.recvfrom(32)
        s.sendto('\x03', ServerAddress)
        break
    except socket.timeout:
        print('waiting for friend to connect to server...')
        
ip = socket.inet_ntoa(data2[:4])
port = int(data2[4:])
print("His Shit: %s:%d" % (ip,port))
myIpPort = s.getsockname()
print("My Shit: %s:%d" % (myIpPort))


s.sendto('\x05', (ip,port))
while True:
    try:
        data3, addr = s.recvfrom(1024)
        if data3 == '\x05':
            print('got connection from friend\n sending confirm...')
            s.sendto('\x05', (ip,port))
            break
    except socket.error:
        s.sendto('\x05', (ip,port))
        print('attempting connection to friend...')
        
while True:
    try:
        data4, addr = s.recvfrom(1024)
        if data4 == '\x06':
            print('got confirm from friend\nsuccess!')
            s.sendto('\x06', (ip,port))
            break
    except socket.error as e:
        s.sendto('\x06', (ip,port))
        print('sending confirm to friend...')
		
