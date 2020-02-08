import socket, threading

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,key,name):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
        
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
        
    def run(self):
        clientName = self.csocket.recv(1024)
        clientName = clientName.decode()
        print (str(clientName) + " has connected from " + str(clientAddress))
        msg = ''
        while True:
            #data = self.csocket.recv(2048)
            #msg = doDecode(data)
            if msg=='bye':
              break
            print (clientName + " > ", msg)
            while True:
                message = raw_input('Me > ')
                if message == '[bye]':
                    message = 'Good Night...'
                    rtnmsg = doEncode(message,key)
                    self.csocket.send(rtnmsg)
                    print("\n")
                    break
                rtnmsg = doEncode(message,key)
                self.csocket.send(rtnmsg)
                
        print ("Client at ", clientAddress , " disconnected...")

       
 
LOCALHOST = "0.0.0.0"
PORT = 48944
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
key = int(raw_input("Enter the master key: "))
name = raw_input('Enter name: ')

print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock,key,name)
    newthread.start()
