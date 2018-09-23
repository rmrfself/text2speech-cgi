import os.path

import cgi
import os

data = cgi.FieldStorage()
params = {}
for key in data.keys():
    params[key] = data[key].value

BASE_FILE_DIR = "tmp"

def  audio_file_path(type, id):
    cur_dir = os.getcwd()
    full_path = os.path.join(cur_dir, "tmp", "%s" % (type), "%s.mp3" % (id))
    if os.path.isfile(full_path):
        return full_path
    else:
        return False

def page_404():
    print("Status:404")
    print("Content-type: text/html")
    print("")

def page_400():
    print("Status:400")
    print("Content-type: text/html")
    print("")

if params.has_key("type") and params.has_key("id"):
    full_path = audio_file_path(params["type"], params["id"])
    if full_path:
        try:
            attachment = open(full_path, "rb")
            buffer = attachment.read()
            print("Content-Type:audio/mpeg3\r\nContent-Disposition:attachment;filename=%s\r\nContent-Transfer-Encoding: binary\r\nContent-Length:%s\r\n\r\n%s" % ("tmp/Item/1.mp3", len(buffer), buffer))
        except IOError:
            page_404()
    else:
        page_404()
else:
    page_400()