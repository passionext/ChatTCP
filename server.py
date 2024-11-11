import csv
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except(Exception,):
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            pass
            # break


# Receiving / Listening Function
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



def receive():
    while True:
        logged = False
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        nickname = None
        # Request And Store Nickname
        while not logged:
            client.send('AUTH'.encode('ascii'))
            authentication = client.recv(1024).decode('ascii')
            logged, nickname = login_function(authentication)
        nicknames.append(nickname)
        clients.append(client)

        # Broadcast Nickname
        #broadcast(f"{nickname} joined!\n".encode('ascii'))
        client.send('CONNECTED'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

thread_rc= threading.Thread(target=receive)
thread_rc.start()
