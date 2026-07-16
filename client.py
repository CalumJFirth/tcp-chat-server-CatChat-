import socket, threading, json

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


#Enter username
message = {
    "type": "username",
    "name": input("Enter username: ") 
}
json_message = json.dumps(message)
client.send(json_message.encode())

#Send Message
while True:
    message = {
        "type": "message",
        "text": input("> ")
    }
    json_message = json.dumps(message)
    client.send(json_message.encode())

    