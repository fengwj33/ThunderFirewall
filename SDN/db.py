#!/usr/bin/python3
import pymysql
from ConnPool import CPool
class DataBase():
    def __init__(self):

        pass
        #self.db = pymysql.connect("45.78.37.244","root","fengwj33","GreenBar" )
    def __del__(self):
        pass
        #self.db.close()
    def addUser(self,userName,Password,UserType):
        sql = "INSERT INTO accounts(UserName,Password,UserType) VALUES ('%s', '%s', %d);" % (userName,Password,UserType)
        self.UPDATE(sql)
    def removeUser(self,userName):
        sql = "DELETE FROM GreenBar.accounts WHERE UserName='%s';" % userName
        self.UPDATE(sql)
    def getUser(self,userName):
        sql="SELECT UserName,Password,UserType FROM GreenBar.accounts WHERE UserName='%s';" % userName
        data=self.SELECT(sql)
        return data

    def validateUser(self,userName,Password):
        sql="SELECT Password,UserType FROM GreenBar.accounts WHERE UserName='%s';" % userName
        data=self.SELECT(sql)
        if len(data)==0:
            return "-1"
        pwd=data[0][0]
        utype=data[0][1]
        if pwd!=Password:
            return "-1"
        return str(utype)

    def getUserMacList(self):
        sql="SELECT UserName,Mac FROM GreenBar.Student;"
        data=self.SELECT(sql)
        return data
    def setUserMac(self,userName,Mac):
        sql="UPDATE GreenBar.Student SET Mac = '%s' WHERE UserName= '%s';" % (Mac,userName)
        self.UPDATE(sql)
    def addStudent(self,userName,Password,StuName):
        self.addUser(userName,Password,1)
        sql = "INSERT INTO Student(Stu_Name,UserName,Mac) VALUES ('%s', '%s','NULL');" % (StuName,userName)
        self.UPDATE(sql)


    def addParent(self,userName,Password,ParentName,Email):
        self.addUser(userName,Password,3)
        sql = "INSERT INTO Parent(ParentName,UserName,EmailAddr) VALUES ('%s', '%s','%s');" % (ParentName,userName,Email)
        self.UPDATE(sql)

    def addTeacher(self,userName,Password,TeacherName,Email):
        self.addUser(userName,Password,2)
        sql = "INSERT INTO Teacher(TeacherName,UserName,EmailAddr) VALUES ('%s', '%s','%s');" % (TeacherName,userName,Email)
        self.UPDATE(sql)
    def removeTeacher(self,userName):
        self.removeUser(userName)
        sql = "DELETE FROM GreenBar.Teacher WHERE UserName='%s';" % userName
        self.UPDATE(sql)
    def editTeacher(self,userName,TeacherName,Email):
        sql="UPDATE GreenBar.Teacher SET TeacherName='%s',EmailAddr='%s' WHERE UserName='%s';" % (TeacherName,Email,userName)
        self.UPDATE(sql)


    def getStudent(self,StuName):
        sql="SELECT UserName FROM GreenBar.Student WHERE Stu_Name='%s';" % StuName
        data=self.SELECT(sql)
        if len(data)==0:
            return None
        else:
            return data[0][0]
    def getStudentName(self,UserName):
        sql="SELECT Stu_Name FROM GreenBar.Student WHERE UserName='%s';" % UserName
        data=self.SELECT(sql)
        if len(data)==0:
            return None
        else:
            return data[0][0]
    def getParent(self,ParentName):
        sql="SELECT UserName FROM GreenBar.Parent WHERE ParentName='%s';" % ParentName
        data=self.SELECT(sql)
        if len(data)==0:
            return None
        else:
            return data[0][0]
    def getTeacher(self,TeacherName):
        sql="SELECT UserName FROM GreenBar.Teacher WHERE TeacherName='%s';" % TeacherName
        data=self.SELECT(sql)
        if len(data)==0:
            return None
        else:
            return data[0][0]
    def getTeacherList(self):
        sql="SELECT TeacherID,UserName,TeacherName,EmailAddr FROM GreenBar.Teacher"
        data=self.SELECT(sql)
        return data
    def setTeacher(self,uName_Stu,uName_Tea):
        sql="UPDATE GreenBar.Student SET TeacherUName='%s'  WHERE UserName='%s';" % (uName_Tea,uName_Stu)
        self.UPDATE(sql)

    def setParent(self,uName_Stu,uName_Par): 
        sql="UPDATE GreenBar.Student SET ParentUName='%s'  WHERE UserName='%s';" % (uName_Par,uName_Stu)
        self.UPDATE(sql)
        sql="UPDATE GreenBar.Parent SET StudentUName='%s'  WHERE UserName='%s';" % (uName_Stu,uName_Par)
        self.UPDATE(sql)
    def getGameServer(self):
        sql="SELECT ServerName,IPAddr FROM GreenBar.GameServer;"
        data=self.SELECT(sql)
        return data
    def setGameServer(self,list):
        sql="truncate table GreenBar.GameServer;"
        self.UPDATE(sql)
        for gs in list:
            sql = "INSERT INTO GreenBar.GameServer(ServerName,IPAddr) VALUES ('%s', '%s');" % (gs[0],gs[1])
            self.UPDATE(sql)
        
    def getBlockList(self):
        sql="SELECT BlockName,IPAddr FROM GreenBar.Block;"
        data=self.SELECT(sql)
        return data
    def setBlockList(self,list):
        sql="truncate table GreenBar.Block;"
        self.UPDATE(sql)
        for gs in list:
            sql = "INSERT INTO GreenBar.Block(BlockName,IPAddr) VALUES ('%s', '%s');" % (gs[0],gs[1])
            self.UPDATE(sql)

    '''def insertLog(StuName,timeID,time,Byte):
        sql = "INSERT INTO GreenBar.OnlineLog(StudentUName,Time,TimeID,Byte) VALUES ('%s', '%s', %d,%d);" % (gs[0],gs[1])'''
    def getLog(self,StuName):
        sql="SELECT TimeID,Time,Byte FROM GreenBar.OnlineLog WHERE StudentUName='%s';" % StuName
        data=self.SELECT(sql)
        return data
    def SELECT(self,query):
        db = CPool.getConn()
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        CPool.returnCon(db)
        return data
    def UPDATE(self,query):
        db = CPool.getConn()
        cursor = db.cursor()
        try:
            cursor.execute(query)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        CPool.returnCon(db)

