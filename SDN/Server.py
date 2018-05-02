#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import pickle
import sys
import MainController
web.config.debug = False
controller=MainController()
controller.run()
urls = (
    "/","login",
    "/login", "login",
    "/regMac", "regMac"
)
class login:
    def GET(self):
        return ""
    def POST(self):
        return ""
class regMac:
    def GET(self):
        if web.input().__len__()!=0:
            if web.input()["userName"]=="del":
            username=web.input()["userName"]
            password=web.input()["password"]
            utype=controller.db.validateUser(username,password)
            if utype=="-1":
                return "Error"
            return str(utype)