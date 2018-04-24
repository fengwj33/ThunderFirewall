#!/usr/bin/python3
import pymysql
db=None


def addUser(userName,Password,UserType):
    sql = "INSERT INTO accounts(UserName,Password,UserType) VALUES ('%s', '%s', %d);" % (userName,Password,UserType)
    UPDATE(sql)

def getUser(userName):
    sql="SELECT UserName,Password,UserType FROM GreenBar.accounts WHERE UserName='%s';" % userName
    data=SELECT(sql)
    return data

def addStudent(userName,Password,StuName):
    addUser(userName,Password,2)
    sql = "INSERT INTO Student(Stu_Name,UserName) VALUES ('%s', '%s');" % (StuName,userName)
    UPDATE(sql)

def addParent(userName,Password,ParentName,Email):
    addUser(userName,Password,3)
    sql = "INSERT INTO Parent(ParentName,UserName,EmailAddr) VALUES ('%s', '%s','%s');" % (ParentName,userName,Email)
    UPDATE(sql)

def addTeacher(userName,Password,TeacherName,Email):
    addUser(userName,Password,3)
    sql = "INSERT INTO Teacher(TeacherName,UserName,EmailAddr) VALUES ('%s', '%s','%s');" % (TeacherName,userName,Email)
    UPDATE(sql)

def getStudent(StuName):
    sql="SELECT UserName FROM GreenBar.Student WHERE Stu_Name='%s';" % StuName
    data=SELECT(sql)
    if len(data)==0:
        return None
    else:
        return data[0][0]
def getStudentName(UserName):
    sql="SELECT Stu_Name FROM GreenBar.Student WHERE UserName='%s';" % UserName
    data=SELECT(sql)
    if len(data)==0:
        return None
    else:
        return data[0][0]
def getParent(ParentName):
    sql="SELECT UserName FROM GreenBar.Parent WHERE ParentName='%s';" % ParentName
    data=SELECT(sql)
    if len(data)==0:
        return None
    else:
        return data[0][0]
def getTeacher(TeacherName):
    sql="SELECT UserName FROM GreenBar.Teacher WHERE TeacherName='%s';" % TeacherName
    data=SELECT(sql)
    if len(data)==0:
        return None
    else:
        return data[0][0]
def setTeacher(uName_Stu,uName_Tea):
    sql="UPDATE GreenBar.Student SET TeacherUName='%s'  WHERE UserName='%s';" % (uName_Tea,uName_Stu)
    UPDATE(sql)

def setParent(uName_Stu,uName_Par): 
    sql="UPDATE GreenBar.Student SET ParentUName='%s'  WHERE UserName='%s';" % (uName_Par,uName_Stu)
    UPDATE(sql)
    sql="UPDATE GreenBar.Parent SET StudentUName='%s'  WHERE UserName='%s';" % (uName_Stu,uName_Par)
    UPDATE(sql)
def getGameServer():
    sql="SELECT ServerName,IPAddr FROM GreenBar.GameServer;"
    data=SELECT(sql)
    return data
def setGameServer(list):
    sql="truncate table GreenBar.GameServer;"
    UPDATE(sql)
    for gs in list:
        sql = "INSERT INTO GreenBar.GameServer(ServerName,IPAddr) VALUES ('%s', '%s');" % (gs[0],gs[1])
        UPDATE(sql)
    
def getBlockList():
    sql="SELECT BlockName,IPAddr FROM GreenBar.Block;"
    data=SELECT(sql)
    return data
def setBlockList(list):
    sql="truncate table GreenBar.Block;"
    UPDATE(sql)
    for gs in list:
        sql = "INSERT INTO GreenBar.Block(BlockName,IPAddr) VALUES ('%s', '%s');" % (gs[0],gs[1])
        UPDATE(sql)

def insertLog(StuName,timeID,time,Byte):
    sql = "INSERT INTO GreenBar.OnlineLog(StudentID) VALUES ('%s', '%s');" % (gs[0],gs[1])
def opendb():
    global db
    db = pymysql.connect("45.78.37.244","root","fengwj33","GreenBar" )
def closedb():
    global db
    db.close()
def SELECT(query):
    global db
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data
def UPDATE(query):
    global db
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()


opendb()
data=getUser("Admin")
 
print (data)
#addStudent("S1","123","alice")
#addParent("P1","123","jack","123@ww.com")
setParent("alice","jack")
 
print (data)
closedb()