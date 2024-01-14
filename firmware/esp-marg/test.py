import socket
import time

HOST = "192.168.0.201"
PORT = 3333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
start = time.time()
i = 0
while True:
    i += 1
    sock.sendall(b"r")
    data = sock.recv(20)
    print(f"Received {data!r}")
    if i > 100:
        break;
stop = time.time()
print(stop - start)

