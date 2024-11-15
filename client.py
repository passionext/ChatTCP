import socket
import threading

import rsa



# Connecting To Server. Create a socket with:
# socket.AF_INET - address family is IPv4
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM
# A non-blocking socket is a socket that does not block the thread when it is waiting for data. This is useful for
# applications that need to be responsive to other events, such as user input or to handle multiple clients

# Set nickname and public key.
## IF HARD-CODED-->public_key = ' '


class SecureClient:
    def __init__(self, server_host='127.0.0.1', server_port=55555):
        self.server_host = server_host
        self.server_port = server_port
        with open('public_key.pem', 'rb') as f:
            self.public_key = rsa.PublicKey.load_pkcs1(f.read())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.authenticated = False
        self.nickname = ''

    # Listening to Server and Sending Nickname
    def receive(self):
        while True:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = self.client_socket.recv(2048).decode('utf-8')
            match message:
                case 'AUTH':
                    # Choosing Nickname
                    self.nickname = input("Enter the nickname: \n")
                    password = input("Enter password: \n")
                    authentication = self.nickname + "/" + password
                    self.client_socket.send(authentication.encode('utf-8'))
                case 'CONNECTED':
                    self.authenticated = True
                    print('You are connected to the server!')
                case _:
                    print(message)

    # Sending Messages To Server
    def write(self):
        while True:
            try:
                if self.authenticated:
                    message = '{}: {}'.format(self.nickname, input(''))
                    encrypted_message = rsa.encrypt(message.encode('utf-8'), self.public_key)
                    self.client_socket.send(encrypted_message)
                else:
                    continue
            except (UnicodeDecodeError, KeyboardInterrupt, ConnectionResetError, UnicodeEncodeError, OverflowError):
                print('Some error occurred.')
                pass

    def start(self):
        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()





client = SecureClient()
client.start()
