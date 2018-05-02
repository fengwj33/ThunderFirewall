#!/usr/bin/python3
import socket
import pickle
import struct
import threading
def send(csocket,msg):
    head=struct.pack('Q',len(msg))
    csocket.send(head)
    csocket.send(msg)
def rcv(csocket):
    rval=bytes()
    length=csocket.recv(8)
    if len(length)==0:
        return rval
    length=struct.unpack('Q',length)
    bsize=1024
    rem=length[0]
    while rem!=0:
        if rem>bsize:
            temp=csocket.recv(bsize)
        else:
            temp=csocket.recv(rem)
        rem-=len(temp)
        rval+=temp
    return rval 
def rscr(csocket):
    while True:
        msg=rcv(csocket)
        print(msg.decode("utf-8"))
        print("#")


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host="0.0.0.0"
port=2345
s.connect((host,port))
print(">>",end="")
echothread=threading.Thread(target=rscr,args=(s,))
echothread.start()

while True:
    
    inp=input()
    send(s,inp.encode("utf-8"))
