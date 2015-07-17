#!/usr/bin/env python
import urllib
import json
from x100.x100util import create_request_info

def http_callback(url, info):
    request_url = url + '?' + info
    request = urllib.request.Request(request_url)
    with urllib.request.urlopen(request) as f:
        return json.loads(f.read().decode('utf-8'))

def video_bitrate_add(url, uuid, bitrate):
    #url = 'http://10.221.193.196:5000/interface/video_uuid_bitrate_add'
    #http://10.221.193.196:5000/interface/video_uuid_bitrate_add?uuid=ytE3V3GyJigi2sqeBK&bitrate=20
    info = 'bitrate=' + bitrate + '&uuid=' + uuid
    return http_callback(url, info)

def video_status_set(url, uuid, status, bitrate=None):
    if bitrate is not None:
        info = create_request_info(uuid=uuid, bitrate=bitrate, status=status)
    else:
        info = create_request_info(uuid=uuid, status=status)
    return http_callback(url, info)
