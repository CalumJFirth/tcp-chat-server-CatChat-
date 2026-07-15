import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5000))
print("Connected!")

def recieve_msg():
    while True:
        message = client.recv(1024)

        if not message:
            print("Disconnected from the server")
            break
        print(message.decode())

thread = threading.Thread(
    target=recieve_msg,
    args=()
)
thread.start()
    
while True:
    msg = input("> ")
    client.send(msg.encode())

    