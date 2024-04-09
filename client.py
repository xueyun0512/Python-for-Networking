import threading 
import socket

nickname = input("What is your nickname?")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',12345))



def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            #see the message broadcasted from the server
            else:
                print(message)

        except:
            print("An error occured")
            break

# when the client is writing something, the client's nickname is displayed
def write():
    while True:
        message = f'{nickname}:{input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


