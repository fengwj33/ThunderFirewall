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
        #threading.Thread(target=SDNCtrl.rcvthread,args=(self,)).start()

        self.updateCheckTable(app.gameserverList)
        self.addUser(app.userList)


    def rcvthread(self):
        while True:
            data=rcv(self.csocket)
            if len(data)==0:
                app.unregctrl(self)
                return
            log("rcv:"+data.decode("utf-8"))
    def getRcv(self):
        data=rcv(self.csocket)
        if len(data)==0:
            app.unregctrl(self)
            return ""
        return data.decode("utf-8")

    def updateCheckTable(self,iplist):
        cmd="updateCheckTable"
        for gs in iplist:
            cmd=cmd+" "+ gs[1]
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def addUser(self,userlist):
        for user in userlist:
            cmd="addUser "+user[0]+" "+user[1]
            send(self.csocket,cmd.encode("utf-8"))
            retdata=self.getRcv()
            log("rcv:"+retdata)
    def addOneUser(self,username,mac):
        cmd="addUser "+username+" "+mac
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def removeUser(self,userName):
        cmd="removeUser "+userName
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def updateUser(self,username,mac):
        cmd="updateUser "+username+" "+mac
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def getflow(self,username):
        cmd="getflow "+username
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        return int(retdata)
    def lockUser(self,userName):
        cmd="lock "+userName
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def unlockUser(self,userName):
        cmd="unlock "+userName
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        log("rcv:"+retdata)
    def getLog(self):
        cmd="getLog"
        send(self.csocket,cmd.encode("utf-8"))
        retdata=self.getRcv()
        return retdata

class MainController():
    
    def __init__(self):
        self.db=db.DataBase()
        self.sdnctrls=set()
        self.gameserverList=self.db.getGameServer()
        self.userList=self.db.getUserMacList()
        cfg=self.db.getCfg()

        self.onlineTime=int(cfg[0][0])
        self.sleepTime=int(cfg[0][1])
        #self.db.clearLog()
        self.logcycle=2
        self.logtimer=self.logcycle
        self.usertimer={}


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
            ctl.addOneUser(userName,'NULL')
    
    def removeStudent(self,userName):
        
        pname=self.db.getStuParent(userName)
        if pname != 'NONE':
            self.db.removeParent(pname)
        self.db.removeStudent(userName)
        for ctl in self.sdnctrls:
            ctl.removeUser(userName)

    def setGameServer(self,iplist):
        self.db.setGameServer(iplist)
        self.gameserverList=self.db.getGameServer()
        for ctl in self.sdnctrls:
            ctl.updateCheckTable(self.gameserverList)



    def getSwitchLog(self):
        logs=[]
        c=0
        for ctl in self.sdnctrls:
            sname="SWITCH$"+str(c)
            log=ctl.getLog()
            logs.append([sname,log])
            c=c+1
        return logs














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
        while True:
            time.sleep(5)
            self.logtimer=self.logtimer-1
            for usr in self.userList:
                usrname=usr[0]
                self.usertimer.setdefault(usrname,[0,self.onlineTime,False])
                flows=0
                for ctl in self.sdnctrls:
                    flows = flows+ctl.getflow(usrname)
                self.usertimer[usrname][0]=self.usertimer[usrname][0]+flows
                
                if flows!=0:
                    if self.usertimer[usrname][2]==False:
                        self.usertimer[usrname][1]=self.usertimer[usrname][1]-1
                        if self.usertimer[usrname][1]<0:
                            self.usertimer[usrname][2]=True
                            self.usertimer[usrname][1]=-self.sleepTime
                            for ctl in self.sdnctrls:
                                ctl.lockUser(usrname)
                else:
                    self.usertimer[usrname][1]=self.usertimer[usrname][1]+1
                    if self.usertimer[usrname][1]>self.onlineTime:
                        self.usertimer[usrname][1]=self.onlineTime
                    if self.usertimer[usrname][1]>0 and self.usertimer[usrname][2]==True:
                        self.usertimer[usrname][1]=self.onlineTime
                        self.usertimer[usrname][2]=False
                        for ctl in self.sdnctrls:
                            ctl.unlockUser(usrname)
            print(self.usertimer['S2'])
            if self.logtimer==0:
                self.logtimer=self.logcycle
                self.updatelog()
            

    
    def updatelog(self):
        print("updating")
        for usr in self.userList:
            usrname=usr[0]
            self.usertimer.setdefault(usrname,[0,self.onlineTime,False])
            flows=self.usertimer[usrname][0]
            self.usertimer[usrname][0]=0
            loctime=time.asctime( time.localtime(time.time()))
            self.db.insertLog(usrname,loctime,flows)
        

    def run(self):

        threading.Thread(target=MainController.connectCtrl,args=(self,)).start()
        #threading.Thread(target=MainController.logThread,args=(self,)).start()

#controller=MainController()
#controller.run()