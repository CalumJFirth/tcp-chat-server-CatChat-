import socket, threading, json

#Set up initial server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()
print("Starting Server")


def send_message(message, sender):
    for client in clients:
        if client != sender:
            client.sendall(json.dumps(message).encode())
            print(message["text"])
                

def handle_client(client, clients):
    while True:
        data = client.recv(1024)
        if data == b'':
            print("Client Disconnected")
            break
        
        text = data.decode()
        json_message = json.loads(text)


        if json_message["type"] == "username":
            clients[client]["username"] = json_message["name"]
            
            
    
        if json_message["type"] == "message":
            send_message(json_message, client)
                    
    clients.remove(client)
    client.close()
    

clients = {}

while True:
    client, addr = server.accept()
    print("Connected:", addr)

    clients[client] = {
        "username":None
        }

    thread = threading.Thread(
        target=handle_client,
        args=(client, clients)
    )
    thread.start()
    print("Ready for another client")


