import socket

class Server():
    '''
    the uhp server class
    '''

    def __init__(self, port):
        self.sUdp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sUdp.bind('', port)
        self.sUdp.settimeout(3)
        self.pools = {}
        self.ipsToHandle = {}
        self.alive = True
    
    def pack_addr(self, addr):
        return str(socket.inet_aton(addr[0])) + str(addr[1])
    
    def handle_ack(self, addr):
        self.ipsToHandle[addr] = 1
        result = self.sUdp.sendto('\x02', addr) == 1
        if(result):
            self.ipsToHandle[addr] = 2
        return result
    
    def pool_connect(self, pool, addr):
        if addr in self.ipsToHandle:
            if self.ipsToHandle[addr] == 2:
                if pool in self.pools:
                    self.pools[pool].append(addr)
                else:
                    self.pools[pool] = [addr]
                result = self.sUdp.sendto('\x04' + str(pool), addr) == len(pool)+1
                if(result):
                    self.ipsToHandle[addr] = 4
        return result
    
    def pool_handler(self, pool):
        cur_pool = self.pools[pool]
        if len(cur_pool) == 2:
            result = self.sUdp.sendto(self.pack_addr(cur_pool[0]), cur_pool[1])
            if(result != len(self.pack_addr(cur_pool[0]))):
                raise socket.error("pool handler: " + cur_pool[1])
            result = self.sUdp.sendto(self.pack_addr(cur_pool[1]), cur_pool[0])
            if(result != len(self.pack_addr(cur_pool[1]))):
                raise socket.error("pool handler: " + cur_pool[0])
        return True
    
    def main(self):
        while self.alive:
            try:
                data, addr = self.sUdp.recvfrom(256)
                if(data == '\x01'):
                    if(self.handle_ack(addr)):
                        raise socket.error("Send acknowledge error: " + str(addr))
                elif(str(data).startswith('\x03')):
                    if(self.pool_connect(data[1:], addr)):
                        raise socket.error("Send acknowledge on pool: " + str(addr))
            except socket.timeout:
                map(self.pool_handler(), self.pools.keys())
            
            
            
                

        