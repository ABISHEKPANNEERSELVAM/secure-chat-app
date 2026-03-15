import socket
import threading
from encryption import encrypt, decrypt

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def private_message(sender, target_name, message):
    if target_name in names:
        index = names.index(target_name)
        target_client = clients[index]
        target_client.send(encrypt(f"[PRIVATE] {sender} : {message}"))
    else:
        sender_index = names.index(sender)
        clients[sender_index].send(encrypt("User not found."))

def kick_user(target_name):
    if target_name in names:
        index = names.index(target_name)
        target_client = clients[index]
        target_client.send(encrypt("You were kicked by admin"))
        target_client.close()

        clients.remove(target_client)
        names.remove(target_name)

        broadcast(encrypt(f"{target_name} was kicked from the chat"))

def handle(client):
    name = names[clients.index(client)]

    while True:
        try:
            message = decrypt(client.recv(1024))

            if message.startswith("/users"):
                user_list = ", ".join(names)
                client.send(encrypt(f"Online users: {user_list}"))

            elif message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) >= 3:
                    target = parts[1]
                    msg = parts[2]
                    private_message(name, target, msg)

            elif message.startswith("/kick"):
                parts = message.split(" ", 1)
                if len(parts) >= 2:
                    target = parts[1]
                    kick_user(target)

            else:
                print(message)
                broadcast(encrypt(message))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            name = names[index]
            names.remove(name)

            broadcast(encrypt(f"{name} left the chat"))
            break

def receive():
    print("Server started...")

    while True:
        client, address = server.accept()
        print("Connected:", address)

        name = client.recv(1024).decode()

        clients.append(client)
        names.append(name)

        broadcast(encrypt(f"{name} joined the chat"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()