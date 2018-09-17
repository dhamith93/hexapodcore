import sys
import getopt
from server import Server as server

def printHelp():
    print()
    print('  -h: help')
    print('  -v: verbose')
    print('  --ip: <IP address>')
    print('  --port: <Port>')
    print()

def main(argv):
    ip = '192.168.4.1'
    port = 8081
    verbose = False

    try:
        opts, args = getopt.getopt(argv, 'v', ['ip=', 'port='])

        for opt, arg in opts:
            if opt == '-v':
                verbose = True
            elif opt == '-h':
                printHelp()
            elif opt == '--ip':
                ip = arg
            elif opt == '--port':
                port = int(arg) 
    except getopt.GetoptError:
        printHelp()
        sys.exit(2) 

    server.start(server, ip, port, verbose)

main(sys.argv[1:])
