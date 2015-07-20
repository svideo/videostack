#!/usr/bin/env python
import os, sys, re, select, subprocess, io, time, shutil, logging
import urllib.request
from x100.x100config import load_config
from x100.x100util import md5, file_create_time, file_size, non_blocking_handler, create_request_info
from x100.x100http import http_callback, video_status_set, video_bitrate_add

class Transcoder:
    def __init__(self):
        self.config = load_config('conf/transcoder.conf')
        self.bitrate = int(self.config['segment']['vbitrate']) + int(self.config['segment']['abitrate'])
        self._log()

    def _log(self):
        logging.basicConfig(level=logging.INFO)

    def handle_body(self, name, body):
        if name == b'video_id':
            uuid = body.decode().rstrip()
            self.uuid = uuid
            self.init_popen_handler()
            res = video_status_set(self.config['url']['video_status_set'], self.uuid, 'proceed', str(self.bitrate))
            if res['status'] == 'failed':
                logging.error("uuid: %s callbackApi: video_status_set error: %s", self.uuid, res['message'])
                return
        elif(name == b'upload'):
            self.run_cmd_async(body)

    def init_popen_handler(self):
        cmd = self.build_cmd()
        print(cmd)
        p = subprocess.Popen(cmd, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.stdout = p.stdout
        self.stdin  = p.stdin
        self.stdout = non_blocking_handler(self.stdout)
        return

    def target_file(self, filename, file_type):
        basedir = self.config['storage']['release_dir']
        md5_str = md5(filename)

        dir1 = md5_str[:3]
        dir2 = md5_str[3:6]
        dir3 = md5_str[6:9]

        target_dir   = basedir + '/' + file_type + '/' + dir1 + '/' + dir2 + '/' + dir3
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_filename = target_dir + '/' + filename
        request_file_path = '/' + dir1 + '/' + dir2 + '/' + dir3 + '/' + filename
        return (target_filename, request_file_path)

    def run_cmd_async(self, body):
        self.stdin.write(body)
        while True:
            line = self.stdout.read(-1)
            #segment:'/tmp/a_sd_000030.flv' count:30 endedp=24 drop=0
            if line is None:
                break
            line  = line.decode()
            ts_re = re.search("segment:\'(.*?)\'\s+count:(\d+).*", line)
            if ts_re:
                ts_file     = ts_re.group(1)
                file_index  = ts_re.group(2)
                ts_filename = ts_file.split('/')[-1]
                (target_file, storage_path) = self.target_file(ts_filename,'ts')
                shutil.move(ts_file, target_file)
                create_time = file_create_time(target_file)
                filesize    = file_size(target_file)
                bitrate     = self.bitrate
                req_info    = create_request_info(uuid=self.uuid, hostname=self.config['base']['hostname'],\
                                      storage_path=storage_path, frame_count=self.config['segment']['fps_count'],\
                                      file_size=str(filesize), fragment_id=file_index, bitrate=str(bitrate),\
                                      fps=self.config['segment']['fps'], create_time=create_time)

                print(req_info)
                #res = callback_segment_add(self.uuid, req_str)
                res = http_callback( self.config['url']['uuid_segment_add'], req_info)
                if res['status'] == 'success':
                    logging.info("uuid: %s segment: %s callback success", self.uuid, storage_path)
                else:
                    logging.error("uuid:%s segment: %s callback error: %s", self.uuid, storage_path, res['message'])

            snap_re = re.search("snap:\'(.*?)\'\s+count:(\d+).*", line)
            if snap_re:
                snap_img_file = snap_re.group(1)
                snap_index    = snap_re.group(2)
                snap_filename = snap_img_file.split('/')[-1]
                (target_file, request_file) = self.target_file(snap_filename, 'snap')
                print("===========================")
                print(target_file)
                print(request_file)
                print("===========================")
                shutil.move(snap_img_file, target_file)
                #info = 'uuid=' + self.uuid +  '&snap_count=' + snap_index
                info = create_request_info(uuid=self.uuid, snap_count=snap_index)
                print(self.config['url']['video_uuid_snap_count_set'])
                print(info)
                res  = http_callback(self.config['url']['video_uuid_snap_count_set'], info)
                if res['status'] == 'success':
                    logging.info("uuid: %s snap: %s callbackApi: video_uuid_snap_count_set success", self.uuid, snap_filename)
                else:
                    logging.error("uuid:%s snap: %s callbackApi: video_uuid_snap_count_set  error: %s", self.uuid, snap_filename, res['message'])
        return

    def build_cmd(self):
        #target_ts_name, target_snap_name = self.target_filename()
        storage_dir = self.config['storage']['dir']
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        tmp_ts_name = storage_dir + '/' + self.uuid + "_%d.flv"
        tmp_snap_name = storage_dir + '/' + self.uuid + "_%d.jpg"
        vbitrate = self.config['segment']['vbitrate']
        abitrate = self.config['segment']['abitrate']
        segment_time = self.config['segment']['time']
        cmd = ""
        cmd += "ffmpeg -v verbose -i - -map 0 -dn"
        cmd += " -c:v copy -b:v " + vbitrate + 'k' + " -preset fast -s 86x48 "
        cmd += " -pix_fmt yuv420p"
        cmd += " -c:a libfaac -b:a " + abitrate + 'k' + " -ar 32000 -ac 2"
        cmd += " -bsf:v h264_mp4toannexb -f segment -segment_format mpegts -segment_time " + segment_time
        #-bsf:v h264_mp4toannexb -f segment -segment_format mpegts
        cmd += " -y " + tmp_ts_name
        cmd += " -r 0.5 -s 176x144 -y " + tmp_snap_name + " 2>&1"
        if cmd is not None:
            self.cmd = cmd
        else:
            self.cmd = ""
        return cmd

    def __del__(self):
        self.stdin.close()
        while True:
            content = self.stdout.read(-1)
            if not content:
                break
            print(content)
        #video_status_set(url, uuid, status, bitrate=None):
        res = video_status_set(self.config['url']['video_status_set'], self.uuid, 'success')
        if res['status'] == 'failed':
            logging.error('uuid: %s error: %s', self.uuid, res['message'])
        return
