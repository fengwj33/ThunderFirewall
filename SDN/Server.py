#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import pickle
import sys
import json
import MainController
web.config.debug = False
controller=MainController.MainController()
controller.run()

urls = (
    "/Debug","debug",
    "/","login",
    "/login", "login",
    "/regMac", "regMac",
    "/index","index",
    "/ADTeacher","ADTeacher",
    "/ETeacher","ETeacher",
    "/ADStudent","ADStudent",
    "/EStudent","EStudent",
    "/EParent","EParent",
    "/EditRules","EditRules",
    "/StudentLog","StudentLog",
    "/pStudentLog","pStudentLog",
    "/sStudentLog","sStudentLog",
    "/SwitchLog","SwitchLog",
    "/logout","logout",
    "/setnewPassword","setnewPassword",
    "/setnewEmail","setnewEmail",

    "/GetTeacherList","GetTeacherList",
    "/AddTeacher","AddTeacher",
    "/removeTeacher","removeTeacher",
    "/editTeacher","editTeacher",
    "/GetStudentList","GetStudentList",
    "/GetStudentListWP","GetStudentListWP",
    "/AddStudent","AddStudent",
    "/removeStudent","removeStudent",
    "/editStudent","editStudent",
    "/AddParent","AddParent",
    "/GetParentList","GetParentList",
    "/editParent","editParent",
    "/GetGameServerList","GetGameServerList",
    "/SetGameServerList","SetGameServerList",
    "/getLog","getLog",
    "/pgetLog","pgetLog",
    "/sgetLog","sgetLog",
    "/getSwitchLog","getSwitchLog",
    "/setPassword","setPassword",
    "/setEmail","setEmail"

)
app= web.application(urls,globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': False,'UserName':"",'userType':-1})
class login:
    def GET(self):
        if session.login==True:
            raise web.seeother('/index')
        return render.login("none")
    def POST(self):
        username=web.input()["userName"]
        password=web.input()["password"]
        db=controller.getDB()
        utype=db.validateUser(username,password)
        if utype=="-1":
            return render.login("block")
        session.login=True
        session.UserName=username
        session.userType=utype
        raise web.seeother('/index')
class setPassword:
    def POST(self):
        oldPassword=web.input()["oldPassword"]
        newPassword=web.input()["newPassword"]
        username=session.UserName
        db=controller.getDB()
        utype=db.validateUser(username,oldPassword)
        if utype=="-1":
            session.login=False
            return "Fail"
        db.setPassword(username,newPassword)
        return "Success"
class setEmail:
    def POST(self):
        EmailAddr=web.input()["EmailAddr"]
        username=session.UserName
        utype=session.userType
        db=controller.getDB()
        if utype=='2':
            db.setTEmail(username,EmailAddr)
        elif utype=='3':
            db.setPEmail(username,EmailAddr)
        return "success"
    
class debug:
    def GET(self):
        
        return ""
class getLog:
    def GET(self):
        username=web.input()["userName"]
        db=controller.getDB()

        logs=db.getLog(username)
        x=[i for i in range(30)]
        retval={"x":[],"time":[],"value":[]}
        retval["x"]=x
        retval["name"]=db.getStudentName(username)
        l=len(logs)
        retval["value"]=[]
        retval["time"]=[]
        for log in logs:
            retval["value"].append(log[1])
            retval["time"].append(log[0])
        if l<30:
            retval["value"].extend([0 for id in range(30-l)])
            retval["time"].extend(["NULL" for id in range(30-l)])
        return json.dumps(retval)

class pgetLog:
    def GET(self):
        pusername=session.UserName
        
        db=controller.getDB()
        username=db.getParentStu(pusername)
        logs=db.getLog(username)
        x=[i for i in range(30)]
        retval={"x":[],"time":[],"value":[]}
        retval["x"]=x
        retval["name"]=db.getStudentName(username)
        l=len(logs)
        retval["value"]=[]
        retval["time"]=[]
        for log in logs:
            retval["value"].append(log[1])
            retval["time"].append(log[0])
        if l<30:
            retval["value"].extend([0 for id in range(30-l)])
            retval["time"].extend(["NULL" for id in range(30-l)])
        return json.dumps(retval)
class sgetLog:
    def GET(self):
        username=session.UserName
        db=controller.getDB()
        logs=db.getLog(username)
        x=[i for i in range(30)]
        retval={"x":[],"time":[],"value":[]}
        retval["x"]=x
        retval["name"]=db.getStudentName(username)
        l=len(logs)
        retval["value"]=[]
        retval["time"]=[]
        for log in logs:
            retval["value"].append(log[1])
            retval["time"].append(log[0])
        if l<30:
            retval["value"].extend([0 for id in range(30-l)])
            retval["time"].extend(["NULL" for id in range(30-l)])
        return json.dumps(retval)
class getSwitchLog:
    def GET(self):
        logs=controller.getSwitchLog()
        retval={}
        retval["body"]=logs
        return json.dumps(retval)
class index:
    def GET(self):
        if session.login==False:
            raise web.seeother('/')
        if session.userType=='0':
            return render.index("Admin")
        elif session.userType=='1':
            return render.index("Student")
        elif session.userType=='2':
            return render.index("Teacher")
        elif session.userType=='3':
            return render.index("Parent")
        return session.userType
class regMac:
    def GET(self):
        if web.input().__len__()!=0:
            username=web.input()["userName"]
            password=web.input()["password"]
            Mac=web.input()["mac"]
            db=controller.getDB()
            utype=db.validateUser(username,password)
            if utype=="-1":
                return "Error"
            if utype=="1":
                controller.alteruserMac(username,Mac)
                return "success"+Mac
            return "error"+Mac+str(utype)

class ADTeacher:
    def GET(self):
        return render.AddTeacher()
    def POST(self):
        return ""
class ADStudent:
    def GET(self):
        return render.AddStudent()
    def POST(self):
        return ""
class ETeacher:
    def GET(self):
        return render.ETeacher()
    def POST(self):
        return ""
class EStudent:
    def GET(self):
        return render.EditStudent()
    def POST(self):
        return ""
class EParent:
    def GET(self):
        return render.EditParent()
    def POST(self):
        return ""
class EditRules:
    def GET(self):
        return render.AccessRules()
    def POST(self):
        return ""
class StudentLog:
    def GET(self):
        return render.StudentLog()
    def POST(self):
        return ""
class pStudentLog:
    def GET(self):
        return render.pLog()
    def POST(self):
        return ""
class sStudentLog:
    def GET(self):
        return render.sLog()
    def POST(self):
        return ""
class SwitchLog:
    def GET(self):
        return render.getSwitchStatus()
    def POST(self):
        return ""
class setnewPassword:
    def GET(self):
        return render.setPassword()
    def POST(self):
        return ""
class setnewEmail:
    def GET(self):
        return render.setEmail()
    def POST(self):
        return ""

    
class logout:
    def GET(self):
        session.login=False
        raise web.seeother('/login')
class GetTeacherList:
    def GET(self):
        db=controller.getDB()
        data=db.getTeacherList()
        retval={}
        list=[]
        for r in data:
            temp=[]
            for c in r:
                temp.append(c)
            list.append(temp)
        retval["body"]=list
        retjson=json.dumps(retval)
        return retjson
class GetGameServerList:
    def GET(self):
        db=controller.getDB()
        data=db.getGameServer()
        retval={}
        list=[]
        for r in data:
            temp=[]
            for c in r:
                temp.append(c)
            list.append(temp)
        retval["body"]=list
        retjson=json.dumps(retval)
        return retjson
class SetGameServerList:
    def POST(self):
        iplist=json.loads(web.input()["iplist"])
        controller.setGameServer(iplist["body"])
        return "success"
class GetParentList:
    def GET(self):
        db=controller.getDB()
        Teacher=session.UserName
        data=db.getParentList(Teacher)
        retval={}
        list=[]
        for r in data:
            temp=[]
            for c in r:
                temp.append(c)
            list.append(temp)
        retval["body"]=list
        retjson=json.dumps(retval)
        return retjson
class AddTeacher:
    def POST(self):
        UserName=web.input()["UserName"]
        TeacherName=web.input()["TeacherName"]
        Email=web.input()["Email"]
        Password=web.input()["Password"]
        db=controller.getDB()
        db.addTeacher(UserName,Password,TeacherName,Email)
        return "success"
class GetStudentList:
    def GET(self):
        db=controller.getDB()
        print(session.UserName)
        data=db.getStudentList(session.UserName)
        retval={}
        list=[]
        for r in data:
            temp=[]
            for c in r:
                temp.append(c)
            list.append(temp)
        retval["body"]=list
        retjson=json.dumps(retval)
        return retjson
class GetStudentListWP:
    def GET(self):
        db=controller.getDB()
        print(session.UserName)
        data=db.getStudentListWithParent(session.UserName)
        retval={}
        list=[]
        for r in data:
            temp=[]
            for c in r:
                temp.append(c)
            list.append(temp)
        retval["body"]=list
        retjson=json.dumps(retval)
        return retjson
class AddStudent:
    def POST(self):
        UserName=web.input()["UserName"]
        StudentName=web.input()["StudentName"]
        Password=web.input()["Password"]
        Teacher=session.UserName
        controller.addStudent(UserName,Password,StudentName,Teacher)
        return "success"
class AddParent:
    def POST(self):
        UserName=web.input()["UserName"]
        ParentName=web.input()["ParentName"]
        StudentUName=web.input()["StudentUName"]
        Email=web.input()["Email"]
        Password=web.input()["Password"]
        Teacher=session.UserName
        db=controller.getDB()
        db.addParent(UserName,Password,ParentName,Email,Teacher)
        db.setParent(StudentUName,UserName)
        return "success"
class removeStudent:
    def POST(self):
        UserName=web.input()["UserName"]
        controller.removeStudent(UserName)
        return "success"
class editStudent:
    def POST(self):
        UserName=web.input()["UserName"]
        StudentName=web.input()["StudentName"]
        db=controller.getDB()
        db.editStudent(UserName,StudentName)
        return "success"
class removeTeacher:
    def POST(self):
        UserName=web.input()["UserName"]
        db=controller.getDB()
        db.removeTeacher(UserName)
        return "success"
class editTeacher:
    def POST(self):
        UserName=web.input()["UserName"]
        TeacherName=web.input()["TeacherName"]
        Email=web.input()["Email"]
        db=controller.getDB()
        db.editTeacher(UserName,TeacherName,Email)
        return "success"
class editParent:
    def POST(self):
        UserName=web.input()["UserName"]
        TeacherName=web.input()["ParentName"]
        Email=web.input()["Email"]
        db=controller.getDB()
        db.editParent(UserName,TeacherName,Email)
        return "success"
if __name__== "__main__":
    app.run()
