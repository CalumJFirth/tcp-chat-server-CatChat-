import socket, threading, json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5000))
print("Connected!")

def recieve_msg():
    while True:
        data = client.recv(1024)

        if not message:
            print("Disconnected from the server")
            break
        text = data.decode()
        json_message = json.loads(text)

        if json_message["type"] == "message":
            print(json_message["username"] + ": " + json_message["text"])

        if json_message["type"] == "system":
            print(json_message["text"])
 
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

    