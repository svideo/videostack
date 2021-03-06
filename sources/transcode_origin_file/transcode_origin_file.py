#!/usr/bin/env python3
import sys, os, subprocess, re, time, json
import requests
sys.path.append('../x100utils')
from x100config import load_config

class TranscodeOriginFile:
    def __init__(self, **kwargs):
        configfile  = kwargs['configfile']
        video_type  = kwargs['video_type'] # default, movie, sport,
        resolution  = kwargs['resolution'] # SD
        self.conf = load_config(configfile)

        self.need_convert_bitrates = []
        self.video_id    = ""
        self.config      = self.conf[video_type]
        self.input_file  = self.get_video_file()
        self.filename    = self.get_filename(self.input_file)
        self.passlog     = "tmp/" + self.filename + ".passlog"
        self.output_file = "tmp/" + self.filename + ".flv"

    def get_filename(self, file_path):
        res = re.search("([^\/]+)$", file_path)
        if res is None:
            return None
        return res.group(1)

    def request(self, url, **kwargs):
        if 'none' in kwargs:
            kwargs = None

        r = requests.get(url, params=kwargs)
        res = r.json()

        return res

    def get_video_file(self):
        resp = self.request(self.config['get_video_multibitrate_info'], none=None)
        for line in resp:
            self.video_id = line['video_id']
            self.converted_bitrates = line['bitrates']

        file_path = self.config['origin_file_path'] + '/' + self.video_id

        return file_path

    def detect_cmd(self):
        cmd = ""
        cmd += "ffmpeg -i " + self.input_file
        cmd += " -filter_complex \"split=2[v0][v1],"
        cmd += "[v0]scale=\"w=floor\\(iw*288/ih/8\\)*8:h=288\"[o0],"
        cmd += "[v1]crop=64:32:in_w/2:in_h/2,idet[o1]\""
        cmd += " -map [o0] -c:v libx264 -x264opts crf="+ self.config['crf'] + ":ssim -an -f flv -y /dev/null"
        cmd += " -map [o1] -f rawvideo -y /dev/null"
        return cmd

    def forecast_bitrate(self):
        cmd = self.detect_cmd()
        print(cmd)
        res = self.command_exec(cmd)
        for line in res:
            br_re = re.search('bitrate=\s+(.*?)kbits\/s', line)
            if br_re:
                bitrate = br_re.group(1)

        self.bitrate = bitrate
        print( "cif bitrate %s" % (bitrate) )

        return self.calculate_bitrate(1080) # 必须用1080 去侦测一个信息

    def calculate_bitrate(self, resolution):
        return int( (int(resolution)/288)**1.5 * float(self.bitrate) + 0.5 )

    def get_x264opts(self):
        forecast_br = self.forecast_bitrate()
        print("forecast_bitrate %d " % (forecast_br))
        cmd = ""
        #cmd += "bitrate=" + str(forecast_br)
        if forecast_br < 1100:
            cmd += self.config['x264opts_lt1100']
        elif forecast_br > 1700:
            cmd += self.config['x264opts_gt1700']
        else:
            cmd += self.config['x264opts_btw']

        return cmd

    def mediainfo(self):
        pass

    def get_origin_file_bitrate(self):
        return 797

    def get_origin_file_height(self):
        return 720

    def get_origin_file_resolution(self):
        origin_bitrate = self.get_origin_file_bitrate()
        if origin_bitrate >= int(self.config['vbitrate_UHD']):
            return 1080

        if origin_bitrate >= int(self.config['vbitrate_FHD']):
            return 720

        if origin_bitrate >= int(self.config['vbitrate_HD']):
            return 576

        if origin_bitrate >= int(self.config['vbitrate_SD']) or origin_bitrate < int(self.config['vbitrate_SD']):
            return 360

    def serialize_need_convert_types(self):
        # 要根据原视频的的信息来计算出需要转码的类型
        need_convert_types = self.need_convert_types()
        convert_types = []
        for cvt_type in need_convert_types:
            height = self.config['height_' + cvt_type]
            convert_types.append({cvt_type:height})

        return convert_types

    def all_convert_bitrates(self):
        origin_height = self.get_origin_file_height()
        all_convert_bitrates = []
        if origin_height >= int(self.config['height_UHD']):
            all_convert_bitrates.append(self.config['vbitrate_UHD'])

        if origin_height >= int(self.config['height_FHD']):
            all_convert_bitrates.append(self.config['vbitrate_FHD'])

        if origin_height >= int(self.config['height_HD']):
            all_convert_bitrates.append(self.config['vbitrate_HD'])

        if origin_height >= int(self.config['height_SD']) or origin_height < int(self.config['height_SD']):
            all_convert_bitrates.append(self.config['vbitrate_SD'])

        return all_convert_bitrates

    def need_convert_bitrates(self):
        all_convert_bitrates = self.all_convert_bitrates()

        all_convert_bitrates.append('153') # 接口设计不合理吧，返回信息，还需要我做非常多的处理，重复处理,这一步很他妈多余

        need_convert_bitrates = self.list_diff(all_convert_bitrates, self.converted_bitrates)

        self.need_convert_bitrates = need_convert_bitrates
        return need_convert_bitrates

    def need_convert_types(self):
        need_convert_bitrates = self.need_convert_bitrates()
        need_convert_types = []
        for bitrate in need_convert_bitrates:
            need_convert_types.append(self.config['br'+bitrate+'_to_type'])

        return need_convert_types

    def list_diff(self, a, b):
        a = map(str, a)
        b = map(str, b)
        b = set(b)
        return [aa for aa in a if aa not in b]

    def pass1_cmd(self):
        self.x264opts = self.get_x264opts()
        self.origin_height = self.get_origin_file_height()
        print( "pass1 origin file resolution %s" % (self.origin_height) )
        bitrate = self.calculate_bitrate(self.origin_height)
        print("pass1 origin file calculate_bitrate %d " % (bitrate))

        convert_pass1_cmd = ""
        convert_pass1_cmd += "ffmpeg -i " + self.input_file
        convert_pass1_cmd += " -vf yadif"
        convert_pass1_cmd += " -c:v libx264 -x264opts " + "bitrate=" + str(bitrate) + self.x264opts
        convert_pass1_cmd += ":pass=1:stats=" + self.passlog
        convert_pass1_cmd += " -c:a libfdk_aac -profile:a aac_he -b:a " + self.config['abitrate'] + "k"
        convert_pass1_cmd += " -f flv -y /dev/null"

        return convert_pass1_cmd

    def pass2_cmd(self):
        convert_types = self.serialize_need_convert_types()
        print(convert_types)

        convert_pass2_cmd = "";
        convert_pass2_cmd += "ffmpeg -i " + self.input_file
        convert_pass2_cmd += " -filter_complex \"split=" + str(len(convert_types))

        for i in range(len(convert_types)):
            convert_pass2_cmd += "[v" + str(i) + "]"
        convert_pass2_cmd += ","

        for index, line in enumerate(convert_types):
            (convert_type, height)  = list(line.items())[0]
            convert_pass2_cmd += \
                     "[v" + str(index) + "]" + "scale=" + self.config['scale_'+convert_type] + "[o" + str(index) + "],"

        convert_pass2_cmd = re.sub(r",$", "", convert_pass2_cmd)

        convert_pass2_cmd += "\""

        print(convert_types)
        for index, line in enumerate(convert_types):
            (convert_type, height)  = list(line.items())[0]
            print("pass2 convert_type %s height %s" % (convert_type, height))
            bitrate       = str(self.calculate_bitrate(height))
            print("pass2 bitrate %s " % (bitrate))

            convert_pass2_cmd += " -map "
            convert_pass2_cmd += "[o" + str(index) + "]" + " -c:v libx264 -x264opts "
            convert_pass2_cmd += " bitrate=" + bitrate + self.config['x264opts']
            convert_pass2_cmd += ":pass=2:stats=" + self.passlog + ":ssim:psnr"
            convert_pass2_cmd += " -c:a libfdk_aac -profile:a aac_he -b:a " + self.config['abitrate'] + 'k'
            convert_pass2_cmd += " -f segment -segment_format flv -segment_time " + self.config['segment_time']
            convert_pass2_cmd += " -y " + "tmp/" + self.filename + "_" + convert_type + "_%d.flv"

        return convert_pass2_cmd

    def command_exec(self, cmd):
        cmd_output = []
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
        while process.poll() is None:
            line = process.stderr.read(1024).decode("utf-8")
            cmd_output.append(line)

        return cmd_output

    def run(self):
        pass1_cmd = self.pass1_cmd()
        pass2_cmd = self.pass2_cmd()
        ret = subprocess.check_output(pass1_cmd, shell=True)
        if ret == 1:
            print("cmd pass1 %s failed" % (pass1_cmd))
            return

        ret = subprocess.check_output(pass2_cmd, shell=True)
        if ret == 1:
            print("cmd pass2 %s failed" % (pass2_cmd))
            return

        res = request(self.config['add_video_id_transcode_bitrate'],
                      video_id=self.video_id,
                      bitrates=",".join(self.need_convert_bitrates) )
        if res['status'] == 'failed':
            print("api: add_video_id_transcode_bitrate request failed [reason] %s" % (res['message']))
            return

        res = request(self.config['delete_video_multirate'], video_id=self.video_id)
        if res['status'] == 'failed':
            print("api: delete_video_multirate request failed [reason] %s" % (res['message']))
            return

        print("video_file: %s convert success" % (self.input_file))

    def __del__(self):
        pass


if __name__ == "__main__":
    t = TranscodeOriginFile(
            configfile = './conf/transcode_origin_file.conf',
            video_type = 'default',
            resolution = 'SD')
    t.run()
