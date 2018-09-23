# -*- coding: utf-8 -*-
#!D:\Python25\python.exe -u

"""
    This is all coded by xanderzhang@live.com
    copyright by xanderzhang@live.com
"""

from application import Application
import cgi
import cgitb
cgitb.enable()


# init the  tts application .
# all business  logic
application = Application(cgi)
application.dispatch()