import socket
import threading
import time

from person import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNETIONS = 10
BUFSIZ = 512

persons = []
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)  # sätter up servern


def broadcast(msg, name):
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    client = person.client

    # första meddelandet är alltid en människas namn
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    while True:  # lyssnar efter meddelanden
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"):  # dissconnectar om användaren skriver quit
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break
        else:  # otherwise send message to all other clients
            broadcast(msg, name+": ")
            print(f"{name}: ", msg.decode("utf8"))


def wait_for_connection():

    while True:
        try:
            client, addr = SERVER.accept()  # väntar på clienter
            person = Person(addr, client)  # skapar ett person objekt vid anslutningen
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            threading.Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNETIONS)  # öppnar servern för att lyssna efter anslutningar
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = threading.Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
