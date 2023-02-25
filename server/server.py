import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True

    while connected:
        message_length = conn.recv(HEADER).decode(FORMAT)
        message_length = int(message_length)
        msg = conn.recv(message_length).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr} {msg}]")

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("Startar server")
start()
