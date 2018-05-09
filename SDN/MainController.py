#!/usr/bin/python3
import socket
import pickle
import struct
import threading
import db
import time

logEnable=True
def log(str):
    global logEnable
    if logEnable:
        print(str)

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

class SDNCtrl():
    
    def __init__(self,csocket,app):
        app.regctrl(self)
        self.app=app
        self.csocket=csocket
        threading.Thread(target=SDNCtrl.rcvthread,args=(self,)).start()

        self.updateCheckTable(app.gameserverList)
        self.addUser(app.userList)


    def rcvthread(self):
        while True:
            data=rcv(self.csocket)
            if len(data)==0:
                app.unregctrl(self)
                return
            log("rcv:"+data.decode("utf-8"))
    def updateCheckTable(self,iplist):
        cmd="updateCheckTable"
        for gs in iplist:
            cmd=cmd+" "+ gs[1]
        send(self.csocket,cmd.encode("utf-8"))
    def addUser(self,userlist):
        for user in userlist:
            cmd="addUser "+user[0]+" "+user[1]
            send(self.csocket,cmd.encode("utf-8"))
    def removeUser(self,userName):
        cmd="removeUser "+userName
        send(self.csocket,cmd.encode("utf-8"))
    def updateUser(self,username,mac):
        cmd="updateUser "+username+" "+mac
        send(self.csocket,cmd.encode("utf-8"))

class MainController():
    
    def __init__(self):
        self.db=db.DataBase()
        self.sdnctrls=set()
        self.gameserverList=self.db.getGameServer()
        self.userList=self.db.getUserMacList()




    def regctrl(self,ctl):
        self.sdnctrls.add(ctl)
    def unregctrl(self,ctl):
        self.sdnctrls.remove(ctl)

    def getDB(self):
        return self.db
    def alteruserMac(self,username,mac):
        '''
        for u in self.userList:
            if u[0]==username:
                if u[1]!=mac:
                    u[1]=mac    
                    '''
        
        self.db.setUserMac(username,mac)
        self.userList=self.db.getUserMacList()
        for ctl in self.sdnctrls:
            ctl.updateUser(username,mac)

    

    def addStudent(self,userName,Password,StuName,Teacher):
        self.db.addStudent(userName,Password,StuName,Teacher)
        self.userList=self.db.getUserMacList()
        for ctl in self.sdnctrls:
            ctl.addUser(userName,'NULL')
    
    def removeStudent(self,userName):
        self.db.removeStudent(userName)
        for ctl in self.sdnctrls:
            ctl.removeUser(userName)




















    def connectCtrl(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host="0.0.0.0"
        port=2346
        s.bind((host,port))
        s.listen(5)
        while True:
            clientsocket,addr=s.accept()
            print("#SDNController#:",addr,"\t\t[linked]")
            ctl=SDNCtrl(clientsocket,self)


    def logThread(self):
        
        time.sleep(1000)
    def run(self):
        threading.Thread(target=MainController.connectCtrl,args=(self,)).start()

#controller=MainController()
#controller.run()