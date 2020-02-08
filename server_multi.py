#import base64 encoding
import base64

# import socket programming library 
import socket 
  
# import thread module 
from thread import *
import threading 
  
print_lock = threading.Lock() 

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


# thread function 
def threaded(c,key): 
    while True:
        name="ADMIN"
        client_name = c.recv(1024)
        client_name = client_name.decode()
        print(client_name + ' has connected.')
        print('Press [bye] to leave the chat room')
        c.send(name.encode())
        while True:
           message = raw_input('Me > ')
           if message == '[bye]':
               message = 'Good Night...'
           msg = doEncode(message,key)
           c.send(msg)
           print("\n")
           break
        msg = doEncode(message,key)
        c.send(msg)
        message = c.recv(1024)
        message = doDecode(message,key)
        print(client_name + " > " + message)
        #print(client_name, '>', message)
  
    # connection closed 
    c.close() 
  
  
def Main(): 
    host = "10.0.0.4" 

    port = 48944
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port))
    print('', '({})'.format(host))
    key = int(raw_input("Enter the master key: "))
    #name = raw_input('Enter name: ')

    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,key,)) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 
