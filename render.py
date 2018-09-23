#!D:\Python25\python.exe -u
# -*- coding: utf-8 -*-

from kid import Template
"""
    This is all coded by xanderzhang@live.com
    copyright by xanderzhang@live.com
"""

import speech

def set_header():
    print "Content-type: text/xml\r\n"

class Render:
    
    def __init__(self, object):
        self.speech = object
        if not self.speech:
            raise ValueError


    def render(self):
        if self.speech.item_type == speech.TYPE_ITEM:
            return self.item_render()
        if self.speech.item_type == speech.TYPE_SENTENCE:
            return self.sentence_render()


    def item_render(self):
        template = Template(file='views/item.xml', speech_data=self.speech)
        set_header()
        print template.serialize()

    @staticmethod
    def render_400(message="None"):
        set_header()
        template = Template(file='views/400.xml', message=message)
        print template.serialize()
    
    
    @staticmethod
    def render_500(message="None"):
        set_header()
        template = Template(file='views/500.xml', message=message)
        print template.serialize()
        
            
            
        



