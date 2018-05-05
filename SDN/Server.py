#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import pickle
import sys
import MainController
web.config.debug = False
controller=MainController.MainController()
controller.run()

urls = (
    "/","login",
    "/login", "login",
    "/regMac", "regMac"
)
app= web.application(urls,globals())
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
    
if __name__== "__main__":
    app.run()
