#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import os, sys
import time, datetime
import re
from flask import Flask, flash, url_for

# Windows needs stdio set for binary mode.
# Not quite sure. but if StackOverflow says so
# Who am I to argue
try:
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

class FileHelper():
    def upload(self, parameters):
        directory = url_for('static', filename='images/profile/')
        FIELD = "attachmentName"

        if not parameters.has_key(FIELD):
            return False

        fileitem = parameters[FIELD]
        if not fileitem.file:
            return False

        # ts = time.time()
        directory += '/%s' % (str(datetime.datetime.now()).split('.')[0])
        directory = re.sub(r"[ :-]", "", directory)

        # create folder
        if not os.path.exists(directory):
            os.makedirs(directory, 0o755)

        filename = re.sub(r"[ :-]", "", fileitem.filename)

        fout = file(os.path.join(directory, filename), 'wb')

        time.sleep(1)
        while True:
            chunk = fileitem.file.read(100000)
            if not chunk: break
            fout.write(chunk)
        fout.close()
        return os.path.join(directory, filename)
