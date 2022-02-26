import socket
from threading import Thread

def web_task(HOST,PORT):
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    http_socket = HTTPServer((HOST,PORT),server_func.SimpleHTTPRequestHandler)
    http_socket.serve_forever()

def implant_task_socket(port):
    implant_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HOST = "0.0.0.0"
    PORT = port
    implant_socket.bind((HOST,PORT))
    implant_socket.listen()
    while True:
        client,client_addr = implant_socket.accept()

def server_listen(HOST,PORT):
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #HOST = "0.0.0.0"
    #PORT = 12345
    SERVER.bind((HOST,PORT))
    SERVER.listen()
    while True:
        client,client_addr = SERVER.accept()
        FH_RESULTS = open("task-completed.txt",'w')
        msg = client.recv(1024)
        FH_RESULTS.write(msg.decode())
        FH_RESULTS.close()


def main():
    try:
        threads = []
    
        web_thread = Thread(target=web_task,args=('127.0.0.1',9090))
        threads.append(web_thread)
        web_thread.start()

        server_thread = Thread(target=server_listen,args=('127.0.0.1',12345))
        threads.append(server_thread)
        server_thread.start()
    
        for t in threads:
            t.join()
            
    except KeyboardInterrupt:
        for t in threads:
            t.join()
      
if __name__ == "__main__":
    main()
