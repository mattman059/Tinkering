import time, socket, sys, base64

from _thread import *
import threading

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

print_lock = threading.Lock()

print('Setup Server...')
time.sleep(1)
#Get the hostname, IP Address from socket and set Port
soc = socket.socket()
host_name = socket.gethostname()
#ip = socket.gethostbyname(host_name)
ip = "10.0.0.4"
port = 48944
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))
key = int(raw_input("Enter the master key: "))
name = raw_input('Enter name: ')


soc.listen(1) #Try to locate using socket
print('Waiting for incoming connections...')


connection, addr = soc.accept()
print_lock.acquire()
print("Received connection from ", addr[0], "(", addr[1], ")\n")
print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))

#get a connection from client side
client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name + ' has connected.')
print('Press [bye] to leave the chat room')
connection.send(name.encode())
while True:
   message = raw_input('Me > ')
   if message == '[bye]':
      message = 'Good Night...'
      msg = doEncode(message,key)
      connection.send(msg)
      print("\n")
      break
   msg = doEncode(message,key)
   connection.send(msg)
   message = connection.recv(1024)
   message = doDecode(message,key)
   print(client_name + " > " + message)
   #print(client_name, '>', message)
