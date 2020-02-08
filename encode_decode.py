import base64

def doEncode(msg,key):
    msgEncode = msg
    for i in range(1, key):
        msgEncode = base64.b64encode(msgEncode,"utf-8")
        msgEncode = msgEncode[::-1]
        
    print("Succeeded after : " + str(key) + " loops\nMessage is: " + msgEncode)
    return msgEncode
    
def doDecode(encMsg, key):
    msgDecode = encMsg
    for i in range(1,key):
        msgDecode = msgDecode[::-1]
        msgDecode = base64.b64decode(msgDecode)
        
    print("Succeeded after : " + str(key) + " loops\nMessage is: " + msgDecode)

def main():
    key = 15
    a = doEncode("Hello",key)
    doDecode(a,key)

main()
