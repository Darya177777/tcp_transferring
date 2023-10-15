import socket
from _thread import *
from sys import argv
import os
import time
from pathlib import Path
megabyte = 1024 * 1024


def parse(text):
    while text[0] == "0":
        text = text[1:]
    return text


def client_thread(con):
    data = con.recv(4096)
    message = data.decode()
    addr = parse(message)
    con.send("1".encode())
    data = con.recv(13)
    message = data.decode()
    file_size = parse(message)
    con.send("1".encode())
    file_size = int(file_size)
    n = file_size // megabyte
    seconds_init = time.time()
    sec_in = seconds_init
    res_data = 0
    fdir = Path('uploads')
    fdir.mkdir(parents=True, exist_ok=True)
    with open("uploads\\" + addr, "a") as f:
        for i in range(n):
            data = con.recv(megabyte)
            message = data.decode()
            f.write(message)
            con.send("1".encode())
            if (time.time() - sec_in) >= 3:
                print((i - res_data) / 3, "MB/s")
                res_data = i
                sec_in = time.time()
        if file_size % megabyte != 0:
            data = con.recv(megabyte)
            message = data.decode()
            f.write(message)
            con.send("1".encode())
    file_size_end = os.path.getsize("uploads\\" + addr)
    if file_size_end == file_size:
        print("data has received")
    else:
        print("data hasn't received")
    print("Speed:", int(n / (time.time() - seconds_init)), "MB/s")
    con.close()


if __name__ == "__main__":
    script, port = argv
    server = socket.socket()
    hostname = "192.168.1.101"
    print(hostname)
    server.bind((hostname, int(port)))
    server.listen(5)
    print("Server running")
    while True:
        client, _ = server.accept()
        start_new_thread(client_thread, (client,))

