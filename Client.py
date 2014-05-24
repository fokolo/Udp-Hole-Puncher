import socket

class UhpClient():
    '''
    the uhp client class
    '''
    def __init__(self, ServerAddress):
        self.server_address = ServerAddress
        self.sUdp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sUdp.settimeout(3)
    
    def packedToAddr(self, pack):
        ip = socket.inet_ntoa(pack[:4])
        port = int(pack[4:])
        addr = (ip, port)
        return addr
    
    def ServerConnect(self):
        self.sUdp.sendto('\x01', self.server_address)
        while True:
            try:
                data, = self.sUdp.recvfrom(1)
                if data == '\x02':
                    print('connection to server successful')
                    break
            except socket.timeout:
                self.sUdp.sendto('\x01', self.server_address)
                print('attempting connection to server...')
        return True
    
    def PoolConnect(self, pool_id):
        while True:
            try:
                self.sUdp.sendto('\x03' + pool_id, self.server_address)
                data, = self.sUdp.recvfrom(33)
                if(data == '\x04' + pool_id):
                    print('connection to pool successful')
                    break
            except socket.timeout:
                print('attempting connection to pool...')
        return True
    
    def GetFriend(self):
        while True:
            try:
                data, = self.sUdp.recvfrom(32)
                if(str(data).startswith("\x05")):
                    friend_addr = self.packedToAddr(data[1:])
                    break
            except socket.timeout:
                print('waiting for friend to connect')
        return friend_addr
    
    def ConnectFriend(self, friend_addr):
        successes = 0
        fails = 0
        while successes < 2:
            try:
                self.sUdp.sendto('\x06', friend_addr)
                data, = self.sUdp.recvfrom(1)
                if data == '\x06':
                    successes += 1
            except socket.error as e:
                fails += 1
                print('failed connection. ' + e.errno)
        return True
    
    def close_socket(self):
        self.sUdp.close()
        return True







