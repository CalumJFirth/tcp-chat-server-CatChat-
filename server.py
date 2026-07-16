import socket, threading, json

#Set up initial server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()
print("Starting Server")

#Global Data
clients = {}


#Functions
def send_json(client, message):
    client.sendall(json.dumps(message).encode())

def receive_json(data):
    text = data.decode()
    return json.loads(text)

def broadcast(sender, message):
        for client in clients:
            if client != sender:
                send_json(client, message)

def construct_json(type, text, username):
    message = {
        "type": type,
        "text": text,
        "username": username
        }
    return message
            
def handle_joins(sender, message):
    clients[sender]["username"] = message["name"]
    text = "*** " + message["name"] + " has joined the Chat! ***"
    username = clients[sender]["username"]
    message = construct_json("system", text, username)
    broadcast(sender, message)

def handle_leaves(sender):
    text = "*** " + clients[sender]["username"]  + " has left the Chat! ***"
    username = clients[sender]["username"]
    message = construct_json("system", text, username)
    broadcast(sender, message)


def handle_client(client):

    while True:

        data = client.recv(1024)
        if data == b'':
            print("Client Disconnected")
            break

        json_message = receive_json(data)

        if json_message["type"] == "username":
            handle_joins(client, json_message)

        elif json_message["type"] == "message":
            json_message["username"] = clients[client]["username"]
            broadcast(client, json_message)

        elif json_message["type"] == "test":
            print("test")

    
    handle_leaves(client)
    del clients[client]
    client.close()
    
#Main Program
while True:
    client, address = server.accept()
    print("Connected:", address)

    clients[client] = {
        "username":None
        }

    thread = threading.Thread(
        target=handle_client,
        args=(client,)
    )
    thread.start()
    print("Ready for another client")


