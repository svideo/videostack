#!/usr/bin/env python
import hashlib, os, sys, subprocess
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK
from x100.x100config import load_config

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

def request_info_serialize(**kwargs):
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
    storage_path    = '/'+ file_type +'/'+ dir1 +'/'+ dir2 +'/'+ dir3 +'/'+ filename

    target_filename = target_filename.replace('.flv', '.ts')
    storage_path    = storage_path.replace('.flv', '.ts')
    return (target_filename, storage_path)

def flv2ts(flvfile, tsfile):
    flv2ts_cmd = cmd = "ffmpeg -i " + flvfile +" -c copy -bsf:v h264_mp4toannexb -y "+ tsfile +" &> /dev/null"
    retcode = subprocess.check_call(flv2ts_cmd, shell=True)
    os.remove(flvfile)
    return retcode

def build_cmd(video_id):
    config = load_config('conf/transcoder.conf')
    storage_dir = config['storage']['dir']
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    tmp_ts_name = storage_dir + '/' + video_id + "_%d.flv"
    tmp_snap_name = storage_dir + '/' + video_id + "_%d.jpg"
    vbitrate = config['segment']['vbitrate']
    abitrate = config['segment']['abitrate']
    segment_time = config['segment']['time']
    fps       = config['segment']['fps']
    scale     = config['segment']['scale']
    vcodec    = config['segment']['vcodec']
    acodec    = config['segment']['acodec'].strip('"')
    img_fps   = config['snap']['fps']
    img_scale = config['snap']['scale']

    cmd = ""
    cmd += "ffmpeg -v verbose -i -"
    cmd += " -filter_complex \""
    cmd += " [0:v:0]fps=" + fps + ",scale=" + scale + ",split=2[voutA][vtmpB],"
    cmd += " [vtmpB]fps=" + img_fps + ",scale=" + img_scale + "[voutB],[0:a:0]asplit=1[aoutA]"
    cmd += "\" "
    cmd += " -map [voutA] -map [aoutA] -c:v libx264 -x264opts " + vcodec
    cmd += " -c:a " + acodec + " -f segment -segment_format flv -segment_time " + segment_time
    cmd += " -y "+ tmp_ts_name +" -map [voutB] -y " + tmp_snap_name + " 2>&1"

    if cmd is not None:
        cmd = cmd
    else:
        cmd = ""

    return cmd
