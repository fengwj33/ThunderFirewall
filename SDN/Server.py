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


    "/GetTeacherList","GetTeacherList",
    "/AddTeacher","AddTeacher",
    "/removeTeacher","removeTeacher",
    "/editTeacher","editTeacher",
    "/GetStudentList","GetStudentList",
    "/GetStudentListWP","GetStudentListWP",
    "/AddStudent","AddStudent",
    "/removeStudent","removeStudent",
    "/editStudent","editStudent",
    "/AddParent","AddParent"
)
app= web.application(urls,globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': False,'UserName':"",'userType':-1})
class login:
    def GET(self):
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
class debug:
    def GET(self):
        
        return ""
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
if __name__== "__main__":
    app.run()
