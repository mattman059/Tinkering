"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import base64

def doEncode(msg,key):
    msgEncode = msg
    for i in range(1, key):
        msgEncode = base64.b64encode(msgEncode,"utf-8")
        msgEncode = msgEncode[::-1]
        
    #print("Succeeded after : " + str(key) + " loops\nMessage is: " + msgEncode)
    return msgEncode

def doDecode(encMsg, key):
    msgDecode = encMsg
    for i in range(1,key):
        msgDecode = msgDecode[::-1]
        msgDecode = base64.b64decode(msgDecode)
   
    #print("Succeeded after : " + str(key) + " loops\nMessage is: " + msgDecode)
    return msgDecode

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        #print("%s:%s has connected." % client_address)
        #greetz = "Greetings from the cave! Now type your name and press enter!"
        #greetz = doEncode(greetz,key)
        #client.send(greetz)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ)
    clients[client] = name
    print("Name: " + name)
    while True:
        msg = client.recv(BUFSIZ)
        msg = name+" > "+msg
        msg = doDecode(msg,key)
        if msg != "{quit}":
            print("BROADCAST: " + msg)
            msg = name+" > " + msg
            msg = doEncode(msg,key)
            broadcast(msg)
        else:
            
            client.send("{quit}")
            client.close()
            del clients[client]
            leaving=str(name) + " has left chat"
            leaving = doEncode(leaving,key)
            broadcast(leaving)
            break


def broadcast(msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        print("Broadcasting to : " + str(sock))
        sock.send(msg)

        
clients = {}
addresses = {}

HOST = '0.0.0.0'
PORT = 48944
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
key=int(raw_input("Enter master key: "))
if __name__ == "__main__":
    
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
