# telnet program example
import socket, select, string, sys
import base64


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

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

#main function
if __name__ == "__main__":

    host = raw_input("Enter Server IP: ")
    key = int(raw_input("Enter the master key: "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connect to remote host
    try :
        s.connect((host, 48944))
    except :
        print 'Unable to connect'
        sys.exit()
    

    prompt()
    
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                data = doDecode(data,key)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
            
            #user entered a message
            else :
                msg = sys.stdin.readline()
                msg = doEncode(msg,key)
                s.send(msg)
                prompt()
