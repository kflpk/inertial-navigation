import socket

HOST = "192.168.0.201"
PORT = 3333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
while True:
    sock.sendall(b"r")
    data = sock.recv(24).hex()
    print(f"Received {data!r}")

