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
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': False,'UserName':"",'userType':-1})
urls = (
    "/","login",
    "/login", "login",
    "/regMac", "regMac",
    "/ADTeacher","ADTeacher",


    "/GetTeacherList","GetTeacherList",
    "/AddTeacher","AddTeacher",
    "/removeTeacher","removeTeacher"
)
app= web.application(urls,globals())
render = web.template.render('templates/')
class login:
    def GET(self):
        return ""
    def POST(self):
        return ""
class regMac:
    def GET(self):
        if web.input().__len__()!=0:
            username=web.input()["userName"]
            password=web.input()["password"]
            Mac=web.input()["mac"]
            utype=controller.db.validateUser(username,password)
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
class removeTeacher:
    def POST(self):
        UserName=web.input()["UserName"]
        db=controller.getDB()
        db.removeTeacher(UserName)
        return "success"
if __name__== "__main__":
    app.run()
