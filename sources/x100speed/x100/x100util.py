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

def get_target_file(release_dir, filename, file_type):

    md5_str = md5(filename)

    dir1 = md5_str[:3]
    dir2 = md5_str[3:6]
    dir3 = md5_str[6:9]

    target_dir   = release_dir + '/' + file_type + '/' + dir1 + '/' + dir2 + '/' + dir3
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    target_filename = target_dir + '/' + filename
    storage_path    = '/' + dir1 + '/' + dir2 + '/' + dir3 + '/' + filename

    target_filename = target_filename.replace('.flv', '.ts')
    storage_path    = storage_path.replace('.flv', '.ts')
    return (target_filename, storage_path)
