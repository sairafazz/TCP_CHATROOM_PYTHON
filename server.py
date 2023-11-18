import threading
import socket
from array import array

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = {}
messages = array('u')  


def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                remove_client(c)


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        alias = aliases[client]
        broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)
        clients.remove(client)
        del aliases[client]


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
            messages.extend(message.decode('utf-8'))
        except:
            remove_client(client)
            break


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases[client] = alias
        clients.append(client)
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'), client)
        client.send('You are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
