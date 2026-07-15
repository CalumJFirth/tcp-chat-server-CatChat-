import socket, threading

#Set up initial server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()
print("Starting Server")


def handle_client(conn, clients):
    while True:
        message = conn.recv(1024)
        if message == b'':
            print("Client Disconnected")
            break
        print(message.decode())
        for client in clients:
            if client != conn:
                client.sendall(message)
                
    clients.remove(conn)
    conn.close()
    

clients = []

while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    clients.append(conn)

    thread = threading.Thread(
        target=handle_client,
        args=(conn, clients)
    )
    thread.start()
    print("Ready for another client")


