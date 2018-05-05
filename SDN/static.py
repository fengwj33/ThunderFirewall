#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
urls = (
    "/","index"
)
app= web.application(urls,globals())
class index:
    def GET(self):
        web.header('Content-Type','text/html;charset=UTF-8')
        return "index"

if __name__== "__main__":
    app.run()
