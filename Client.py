import socket
import sys


class UhpClient():
    '''
    the uhp client class
    '''
    def __init__(self, server_addr, pool):
        self.server_address = server_addr
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.settimeout(3)
        self.pool_id = pool
        self.alive = True
        self.friend = None

    @staticmethod
    def packet_addr(pack):
        return socket.inet_ntoa(pack[:4]), int(pack[4:])
    
    def connect_server(self):
        self.udp_sock.sendto('\x01', self.server_address)
        while True:
            try:
                data = self.udp_sock.recvfrom(1)[0]
                if data == '\x02':
                    print('connection to server successful')
                    break
            except socket.timeout:
                self.udp_sock.sendto('\x01', self.server_address)
                print('attempting connection to server...')
        return True
    
    def connect_pool(self, pool_id):
        while True:
            try:
                self.udp_sock.sendto('\x03' + pool_id, self.server_address)
                data = self.udp_sock.recvfrom(33)[0]
                if data == '\x04' + pool_id:
                    print('connection to pool successful')
                    break
            except socket.timeout:
                print('attempting connection to pool...')
        return True
    
    def get_friend(self):
        while True:
            try:
                data = self.udp_sock.recvfrom(32)[0]
                if str(data).startswith("\x05"):
                    friend_addr = self.packet_addr(data[1:])
                    break
            except socket.timeout:
                print('waiting for friend to connect')
        return friend_addr
    
    def friend_connect(self, friend_addr):
        successes = 0
        fails = 0
        while successes < 2:
            try:
                self.udp_sock.sendto('\x06', friend_addr)
                data = self.udp_sock.recvfrom(1)[0]
                if data == '\x06':
                    successes += 1
            except socket.error:
                if successes > 0:
                    break
                fails += 1
                print('failed connection. attempting')
        return True

    def init_chat(self):
        self.udp_sock.settimeout(0.0)
        while self.alive:
            try:
                to_print, addr = self.udp_sock.recvfrom(1024)
                sys.stdout.write('\n<%s:%d> said: %s\n' % (self.friend[0], self.friend[1], to_print))
                sys.stdout.flush()
            except socket.error as Ex:
                if Ex.errno == 10035:
                    sys.stdout.write('you say: ')
                    to_send = sys.stdin.readline()[:-1]
                    self.udp_sock.sendto(to_send, self.friend)
                else:
                    raise

    def main(self):
        self.connect_server()
        self.connect_pool(self.pool_id)
        self.friend = self.get_friend()
        if self.friend_connect(self.friend):
            print('success!')
            self.init_chat()
        self.udp_sock.close()