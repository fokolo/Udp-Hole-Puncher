import socket

def encryptAddr(addrT):
    ret = str(socket.inet_aton(addrT[0])) + str(addrT[1])
    return ret

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 20020))

Queue = []
i = 0
while i < 2:
    data, addr = s.recvfrom(4096)
    if data != '\x01':
        continue
    s.sendto('\x02',addr)
    print(addr)
    Queue.append(addr)
    i += 1

print(Queue)

dataToSend = {Queue[0]:encryptAddr(Queue[1]),Queue[1]:encryptAddr(Queue[0])}

for i in dataToSend.keys():
    s.sendto(dataToSend[i], i)

s.settimeout(2)  
while True:
    b = len(dataToSend)
    if b == 0:
        break
    for i in xrange(b):
        try:
            data, addr1 = s.recvfrom(1024)
            if data == '\x03':
                print(dataToSend)
                del dataToSend[addr1]
                print('removing... ')
        except:
            print('retrying ')
    print(dataToSend)
    for i in dataToSend.keys():
        s.sendto(dataToSend[i], i)
            
    
    

