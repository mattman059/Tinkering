import time, socket, sys, base64


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

print('Client Server...')
time.sleep(1)
#Get the hostname, IP Address from socket and set Port
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
#get information to connect with the server
print(shost, '({})'.format(ip))
server_host = raw_input('Enter server\'s IP address:')
name = raw_input('Enter Client\'s name: ')
key = int(raw_input("Enter the master key: " ))
port = 48944
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Connected...\n")
soc.send(name.encode())
msg = soc.recv(1024)
msg = doDecode(msg,key)
print('Enter [bye] to exit.')
while True:

   message = raw_input("Me > ")
   if message == "[bye]":
      message = "Leaving the Chat room"
      msg = doEncode(message,key)
      soc.send(msg)
      print("\n")
      break
   msg = doEncode(message,key)
   soc.send(msg)
   
   #while True:
   message = soc.recv(1024)
   message = doDecode(message,key)
   print(message)
   #print(server_name, ">", message)
   soc.send(msg)
 
