import threading 
import socket

host = '127.0.0.1'
port = 12345

# we create a internet socket using TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))

#when the server is initialised, it has to listen continously 
server.listen()

clients = []
nicknames = []

#send a message to all client connected to the host
# message is already encoded 
def broadcast(message):
    for client in clients:
        client.send(message)


#get the message from the client and broadcast the message to everyone in the chatroom
def handle(client):
    while True:
        try : 
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chatroom'.encode('ascii'))
            nicknames.remove(nicknames)
            break

# as the server is listening all the time, it should receive any message from any client
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        #tell the client to create a nickname
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        #send this to the connecting client 
        client.send('Connected to the server!'.encode('ascii'))

        #the handle function should run all the time so we have to use a thread 
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("The server is listening...")
receive()
