#!D:\Python25\python.exe -u
# -*- coding: utf-8 -*-

import os.path
from time import sleep

import logging
import logging.handlers
import os
import pyTTS
import subprocess

## Environment variable for subprocesses
environ = {'PATH': str(os.getenv('PATH'))}

def prepare_log():
    if not os.path.exists("log"):
        os.mkdir("log")
    if not os.path.isfile("speech.log"):
        try:
            open("log/speech.log", "wb")
        except IOError:
            raise IOError
            return

prepare_log()

LOGGER_FILE_NAME = "log/speech.log"

DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_VOLUME = 100
DEFAULT_RATE = 0

AUDIO_HOST = "192.168.1.195"

LAN_JAN = "ja"
LAN_EN = "en"
LAN_ZH = "zh_cn"

TYPE_ITEM = "Item"
TYPE_SENTENCE = "Sentence"

DEFAULT_VOICE_TYPE = "male"

logging.basicConfig(filename=LOGGER_FILE_NAME, level=logging.INFO, )
voices = {"male":{"ja":"VW Misaki", "en":"VW Paul", "zh":"VW Wang"}, "female":{"ja":"VW Miyu", "en":"VW Kate", "zh":"VW Hui"}}

class Speech:
    # coded by  xanderzhang@live.com
    # id:  integer field ==
    # item_text: text field
    def __init__(self, item_id, item_text, item_language="ja", item_type="Item", male=True):
        self.item_id = item_id
        self.item_text = item_text
        self.item_language = item_language
        self.item_type = item_type
        self.male = male
        self.speech_status = False
        if (not self.item_id) or (not self.item_text):
            raise ValueError
        self.engine = pyTTS.Create()
        self.set_engine_parameters()
        self.make_logger()


    # main function
    # speak to wav file
    def speak(self):
        audio_file = self.translate_audiofile()
        return audio_file

    def translate_audiofile(self):
        # check audio format
        try:
            file_name = "%s.wav" % (self.item_id)
            wave_file_path = os.path.join(self.tmp_audio_dir(), file_name)
            self.engine.SpeakToWave(wave_file_path, unicode(self.item_text, "utf-8"))
            # make sure that wave file is generated
            if self.audio_format == "mp3":
                file_name = "%s.mp3" % (self.item_id)
                mp3_file_path = os.path.join(self.tmp_audio_dir(), file_name)
                self.to_mp3(wave_file_path, mp3_file_path)
                file_path = mp3_file_path
            else:
                file_path = wave_file_path
            self.speech_logger.info("%s - %s - %s - %s - %s" % (self.item_language, self.item_type, self.item_text, self.item_id, self.audio_format))
            self.speech_status = True
        except IOError:
            raise IOError
        return  file_path

    def to_mp3(self, wave_path, mp3_path):
        command = 'lame -m m --cbr -b 32 -q 0 -S %s  %s' % (wave_path, mp3_path)
        sub = subprocess.Popen(command, shell=True, env=environ, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        return sub

    def tmp_audio_dir(self):
        current_dir = os.getcwd()
        work_dir = os.path.join(current_dir, "tmp", self.item_type)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        return work_dir

    
    # set tts engine parameters
    def set_engine_parameters(self):
        if self.engine:
            self.engine.Rate = DEFAULT_RATE
            self.Volume = DEFAULT_VOLUME
            self.audio_format = DEFAULT_AUDIO_FORMAT
            self.select_voice()

    def select_voice(self):
        # male speech KeyError
        if self.male:
            if self.item_language == LAN_JAN:
                self.engine.SetVoiceByName(u"VW Misaki")
            if self.item_language == LAN_EN:
                self.engine.SetVoiceByName(u"VW Paul")
            if self.item_language == LAN_ZH:
                self.engine.SetVoiceByName(u"VW Wang")
        else:
            if self.item_language == LAN_JAN:
                self.engine.SetVoiceByName(u"VW Miyu")
            if self.item_language == LAN_EN:
                self.engine.SetVoiceByName(u"VW Kate")
            if self.item_language == LAN_ZH:
                self.engine.SetVoiceByName(u"VW Hui")
            
    # logger function
    def make_logger(self):
        self.speech_logger = logging.getLogger('speech')
        ch = logging.handlers.RotatingFileHandler(LOGGER_FILE_NAME, maxBytes=1000000000)
        ch.setLevel(logging.INFO)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.speech_logger.addHandler(ch)

    def speech_audio_status(self):
        if self.speech_status:
            return "ok"
        else:
            return "gng"

    def speech_audio_url(self):
        if self.speech_status:
            return "http://%s/fvoice/audio_ws.py?type=%s&id=%s" % (AUDIO_HOST, self.item_type, self.item_id)
        else:
            return ""
            