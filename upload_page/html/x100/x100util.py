#!/usr/bin/env python
import hashlib, os, sys
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK

def md5(filename):
    m = hashlib.md5()
    m.update(filename.encode())
    md5_str = m.hexdigest()
    return md5_str

def file_create_time(afile):
    if not os.path.exists(afile):
        print("file %s not exist" % afile)
        sys.exit(1)
    return str(int(os.path.getctime(afile)))

def file_size(afile):
    if not os.path.exists(afile):
        print("file %s not exist" % afile)
        sys.exit(1)
    statinfo = os.stat(afile)
    return statinfo.st_size

def non_blocking_handler(handler):
    flags = fcntl(handler, F_GETFL)
    fcntl(handler, F_SETFL, flags | O_NONBLOCK)
    return handler

def create_request_info(**kwargs):
    info = ""
    for k, v in kwargs.items():
        info += k + '=' + v + '&'
    return info
