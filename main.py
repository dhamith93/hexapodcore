from server import Server as server


def main():
    server.start('192.168.1.4', 8081)

main()