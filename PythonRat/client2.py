from client_class import *

def main():
    threads = []
    tasking = Thread(target=tasking_thread)
    tasking.daemon = True
    threads.append(tasking)
    tasking.start()

    comms = Thread(target=comms_thread)
    comms.daemon = True
    threads.append(comms)
    comms.start()

    for t in threads:
        t.join()

    

if __name__ == "__main__":
    main()