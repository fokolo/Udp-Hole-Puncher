import socket


class PoolHandle():
    def __init__(self, pool_type, pool_id, udp_sock):
        self.pool_type = pool_type
        self.pool_id = pool_id
        self.pool_members = []
        self.udp_sock = udp_sock
        if pool_type == 'client-server':
            self.pool_server = tuple()

    @staticmethod
    def pack_addr(addr):
        return str(socket.inet_aton(addr[0])) + str(addr[1])

    def set_server(self, server_addr):
        self.pool_server = server_addr

    def add_member(self, member_addr):
        self.pool_members.append(member_addr)

    def send_addr_p2p(self):
        send_queue = []
        if len(self.pool_members) == 2:
            peer1 = self.pool_members[0]
            peer2 = self.pool_members[1]
            send_queue.append(tuple(('\x05' + str(self.pack_addr(peer2)), peer1)))
            send_queue.append(tuple(('\x05' + str(self.pack_addr(peer1)), peer2)))
        return send_queue

    def is_member(self, member):
        return member in self.pool_members

    def broadcast_server(self):
        for member in self.pool_members:
            self.udp_sock.sendto('\x05' + str(self.pack_addr(self.pool_server)), member)

    def send_members(self):
        send = '\x05'
        for member in self.pool_members:
            send += '\x00' + str(self.pack_addr(member))
        self.udp_sock.sendto(send, self.pool_server)