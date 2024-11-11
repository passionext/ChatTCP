import socket
import threading
from time import sleep

# Connecting To Server. Create a socket with:
# socket.AF_INET - address family is IPv4
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
# A non-blocking socket is a socket that does not block the thread when it is waiting for data. This is useful for
# applications that need to be responsive to other events, such as user input or to handle multiple clients

nickname = input("Enter your nickname: ")
AUTHENTICATED = False
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname

            message = client.recv(1024).decode('ascii')
            match message:
                case 'AUTH':
                # Choosing Nickname
                    password = input("Enter password: \n")
                    authentication = nickname + "/" + password
                    client.send(authentication.encode('ascii'))

                case 'CONNECTED':
                    global AUTHENTICATED
                    AUTHENTICATED = True
                    print('You are connected to the server!')

                case _:
                    print(message)

        except (Exception,):
            # Close Connection When Error
            print("An error occured! Connection aborted.")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        if AUTHENTICATED:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))
        else:
            continue

# Starting Threads For Listening And Writing

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()