#!/usr/bin/env python
import urllib
import json
from x100utils.x100util import request_info_serialize

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

def update_video_status(url, video_id, status, bitrate=None):
    if bitrate is not None:
        info = request_info_serialize(video_id=video_id, bitrate=bitrate, status=status)
    else:
        info = request_info_serialize(video_id=video_id, status=status)
    return http_callback(url, info)
