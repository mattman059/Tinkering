import socket, threading
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


def send(key):
    while True:
        msg = raw_input('')
        msg = doEncode(msg,key)
        cli_sock.send(msg)

def receive(key):
    while True:
        data = cli_sock.recv(1024)
        data = doDecode(data,key)
        print(data)

if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key = int(raw_input("Enter the master key: "))
    name = raw_input("Enter your name: ")
    
    # connect
    HOST = '10.0.0.4'
    PORT = 48944
    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')
    
    #name = doEncode(name,key)
    cli_sock.send(name)

    #print("Starting sender")
    thread_send = threading.Thread(target = send, args = (key,))
    thread_send.start()

    #print("Starting receiver")
    thread_receive = threading.Thread(target = receive, args = (key,))
    thread_receive.start()
