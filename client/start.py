import time
from threading import Thread

from client import Client

name = input("Skriv namn: ")
c1 = Client(name)


def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # uppdaterar varje 1/10 av sekund
        new_messages = c1.get_messages()  # hämtar meddelanden
        msgs.extend(new_messages)  # lägger till i en lista

        for msg in new_messages:  # skriver ut meddelanderna från listan
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

while True:
    message = input()
    c1.send_message(message)
    if message == "{quit}":
        break

