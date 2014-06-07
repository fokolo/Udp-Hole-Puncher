from Client import *
from Server import *
import sys


def print_usage():
    print("Usage:  %s -c <Server_IP:Port> <Pool_ID>\n\t%s -s <Server_Port>\n\n\tOptions:\n\t-c Starts Uhp in client mode\n\t-s Starts Uhp in server mode" % (sys.argv[0], sys.argv[0]))


def handle_client(pool_id, addr):
    client = UhpClient(addr, pool_id)
    client.main()


def handle_server(port):
    server = UhpServer(port)
    server.main()

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 3 and sys.argv[1] == '-s':
        try:
            print("Server start-up with port %d\n" % int(sys.argv[2]))
            handle_server(int(sys.argv[2]))
        except:
            print_usage()
            raise
    elif len(sys.argv) == 4 and sys.argv[1] == '-c':
        try:
            addr = (str(sys.argv[2]).split(':')[0], int(str(sys.argv[2]).split(':')[1]))
            print("Client start-up with pool id:%s and server %s:%d\n" % (sys.argv[3], addr[0], addr[1]))
            handle_client(sys.argv[3], addr)
        except:
            print_usage()
            raise
    else:
        print_usage()