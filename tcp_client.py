import socket
from sys import argv
import os

gigabyte = 1024 * 1024 * 1024


def client():
    script, addr, hostname, port = argv
    client = socket.socket()
    client.connect((hostname, int(port)))
    send_addr = "0" * (4096 - len(addr)) + addr
    client.send(send_addr.encode())
    client.recv(1)
    file_size = os.path.getsize(addr)
    send_size = "0" * (13 - len(str(file_size))) + str(file_size)
    client.send(send_size.encode())
    client.recv(1)
    with open(addr, "r") as f:
        n = file_size // gigabyte
        for i in range(n):
            message = f.read(gigabyte)
            client.send(message.encode())
            client.recv(1)
        if file_size % gigabyte != 0:
            message = f.read(file_size % gigabyte)
            client.send(message.encode())
            client.recv(1)
        print("Server sent all")
        client.close()


if __name__ == "__main__":
    client()
