import pymysql
import threading  
class ConnPool():
    
    def __init__(self):
        self.mutex = threading.Lock()
        self.free=[]
        print("Creating Connection Pool...")
        self.pt=0
        for i in range(0,1):
            cn=pymysql.connect("45.78.37.244","root","fengwj33","GreenBar" )
            self.free.append(cn)
        print("Creating Connection Pool...finish")
    def getConn(self):
        #self.mutex.acquire()
        if self.pt==-1:
            cn=pymysql.connect("45.78.37.244","root","fengwj33","GreenBar" )
            return cn
        retval=self.free[self.pt]
        self.free.remove(retval)
        self.pt=self.pt-1
        #self.mutex.release()
        return retval
    def returnCon(self,connection):
        #self.mutex.acquire()
        self.free.append(connection)
        self.pt=self.pt+1
        #self.mutex.release()
CPool=ConnPool()