#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from FlaskServer import app
import FlaskServer.oem_copy as oem_copy

if __name__ == '__main__':
   oem_copy
   WSGIServer(app, bindAddress='/tmp/fcgi.sock',multithreaded=False,maxThreads=5,multiprocess=False).run()