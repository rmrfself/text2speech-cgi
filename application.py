#!D:\Python25\python.exe -u
# -*- coding: utf-8 -*-

from render import Render
from speech import Speech

class Application:

    def __init__(self, cgi):
        self.cgi = cgi
        self.params = {}
        self.parse_params()

    def parse_params(self):
        data = self.cgi.FieldStorage()
        for key in data.keys():
            value = data[key].value
            self.params[key] = value


    def dispatch(self):
        if (not self.params.has_key("id")) or (not self.params.has_key("type") or (not self.params.has_key("text"))):
            return Render.render_400()
        try:
            pa = self.params
            speech_obj = Speech(pa["id"], pa["text"], pa["lan"], pa["type"])
            speech_obj.speak()
            # response back to client
            response = Render(speech_obj)
            return response.render()
        except Exception, e:
            return Render.render_400(e)
        
