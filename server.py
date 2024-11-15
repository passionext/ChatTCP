import argparse
import csv
import rsa
import socket
import threading

from InquirerPy import prompt

clients = []
nicknames = []


# Load the private and public key
with open('public_key.pem', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())
with open('private_key.pem', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())



def login_function(authentication):
    authentication = authentication.split('/')
    username = authentication[0]
    password = authentication[1]
    matching_creds = False
    with open ('database.csv', 'r') as file:
        dict_reader = csv.DictReader(file)
        list_of_dict = list(dict_reader)
        for element in list_of_dict:
            for key,value in element.items():
                if key == username and value == password:
                    matching_creds = True
    if matching_creds:
        print(f'User named {username} has authenticated!')
        return True, username
    else:
        print(f'User named {username} failed the authentication!')
        return False, "null"


class SecureServer:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.public_key = public_key
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = clients
        self.nicknames = nicknames

    def broadcast(self,message):
        for client in self.clients:
            client.send(message)

    # Handling Messages From Clients
    def handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                encrypted_message = client.recv(2048)
                message = rsa.decrypt(encrypted_message, self.private_key)

                self.broadcast(message)
            except(OSError, ValueError, KeyboardInterrupt):
                # Removing And Closing Clients
                index = self.clients.index(client)
                clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('utf-8'))
                self.nicknames.remove(nickname)
                print('Something went wrong. It\'s very likely that the users has disconnected.')
                pass
                # break
    def receive(self, client, address):
        while True:
            logged = False
            # Accept Connection
            print("Connected with {}".format(str(address)))
            nickname = None
            # Request And Store Nickname
            while not logged:
                client.send('AUTH'.encode('utf-8'))
                authentication = client.recv(2048).decode('utf-8')
                logged, nickname = login_function(authentication)
            self.nicknames.append(nickname)
            self.clients.append(client)

            # Broadcast Nickname
            # broadcast(f"{nickname} joined!\n".encode('utf-8'))
            client.send('CONNECTED'.encode('utf-8'))
            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
            break

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.receive(client_socket, addr)


# Receiving / Listening Function


server = SecureServer()
server.start()