from client_class import *
from threading import Thread

def main():
    server_addr = '10.0.0.60'
    server_port = 12345
    c = Client('10.0.0.45',54321,server_addr,server_port)

    threads = []
    
    tasking = Thread(target=c.tasking_thread)
    tasking.daemon = True
    threads.append(tasking)
    tasking.start()
 
    comms = Thread(target=c.comms_thread)
    comms.daemon = True
    threads.append(comms)
    comms.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
