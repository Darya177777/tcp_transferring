import socket
from _thread import *
from sys import argv
import os
import time
megabyte = 1024 * 1024


def client_thread(con):
    data = con.recv(4096)
    message = data.decode()
    addr = message
    while addr[0] == "0":
        addr = addr[1:]
    con.send(message.encode())
    data = con.recv(13)
    message = data.decode()
    file_size = message
    while file_size[0] == "0":
        file_size = file_size[1:]
    con.send(message.encode())
    file_size = int(file_size)
    n = file_size // megabyte
    seconds_init = time.time()
    sec_in = seconds_init
    res_data = 0
    with open("uploads\\" + addr, "a") as f:
        for i in range(n):
            data = con.recv(megabyte)
            message = data.decode()
            f.write(message)
            con.send(message.encode())
            res_data += 1
            if (time.time() - sec_in) // 60 >= 3:
                print((i - res_data) / 180 * megabyte, "B/s")
                res_data = i
                sec_in = time.time()
        if file_size % megabyte != 0:
            data = con.recv(megabyte)
            message = data.decode()
            f.write(message)
            con.send(message.encode())
    file_size_end = os.path.getsize("uploads\\" + addr)
    if file_size_end == file_size:
        print("data has received")
    else:
        print("data hasn't received")
    print("Speed:", int(file_size_end / (time.time() - seconds_init)), "B/s")
    con.close()


if __name__ == "__main__":
    script, port = argv
    server = socket.socket()
    hostname = "192.168.1.105"
    server.bind((hostname, int(port)))
    server.listen(5)
    print("Server running")
    while True:
        client, _ = server.accept()
        start_new_thread(client_thread, (client,))
