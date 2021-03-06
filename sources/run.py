#!/usr/bin/env python3
import argparse
from interface.x100speed_interface import *
from transcoder.transcoder import Transcoder
from x100http import  X100HTTP, X100Response
from x100daemon import Daemon

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--daemonize", help="make daemonize", action="store_true")
args = parser.parse_args()

if args.daemonize:
    pidfile = '/var/run/x100speed_transcoder.pid'
    d = Daemon(pidfile)
    d.daemonize()

app = X100HTTP()
app.get("/interface/add_staff_ip",                   add_staff_ip)
app.get("/interface/update_staff_monitor",           update_staff_monitor)
app.get("/interface/get_video_id",                   get_video_id)
app.get("/interface/update_video_status",            update_video_status)
app.get("/interface/get_video_info",                 get_video_info)
app.get("/interface/get_video_multirate_info",       get_video_multirate_info)
app.get("/interface/delete_video_id_multirate",      delete_video_id_multirate)
app.get("/interface/add_video_id_transcode_bitrate", add_video_id_transcode_bitrate)
app.get("/interface/update_video_snap_image_count",  update_video_snap_image_count)
app.get("/interface/get_video_new_snap_image",       get_video_new_snap_image)
app.get("/interface/add_video_segment",              add_video_segment)
app.get("/interface/<play_url>.m3u8",                video_play)
app.get("/interface/<play_url>_<play_bitrate>.m3u8", video_play_child)
app.upload("/upload", Transcoder)
app.static("/", "/data1/hls/segment/", cors="*")
app.run("0.0.0.0", 80)
