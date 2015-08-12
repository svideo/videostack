#!/usr/bin/env python3
import sys, os, subprocess
sys.path.append('../x100utils')
from x100config import load_config

class TranscodeOriginFile:
    def __init__(self, **kwargs):
        configfile = kwargs['configfile']
        self.config = load_config(configfile)
        self.video_type  = kwargs['video_type'] # default, movie, sport,
        self.resolution  = kwargs['resolution'] # SD
        self.video_file  = self.get_video_file()
        self.output_file = "tmp/" + self.video_flv + ".flv"
        self.init_convert_args( video_type=self.video_type, resolution=self.resolution )

    def init_convert_args(self, **kwargs):
        video_type = kwargs['video_type'] # default, moive, sport
        resolution = kwargs['resolution'] # SD, HD
        config = self.config[video_type]

        vbitrate = config['vbitrate_'+resolution]
        abitrate = config['abitrate']
        vcodec   = config['vcodec']
        width    = config['width_'+resolution]
        keyint   = config['keyint']
        self.fps = config['fps']

        self.ffmpeg_vcodec = "libx264 -x264opts bitrate=" + vbitrate + ":keyint=" + keyint + ":" + vcodec
        self.ffmpeg_acodec = "libfdk_aac -profile:a aac_he -b:a" + abitrate
        self.vf = " scale=" + self.width + ":" + self.height


    def get_video_file(self):
        # request api to get file
        return '/data1/queue/ywOVs9MIA8AUUMSSuI'

    def origin_file_analysis(origin_file):
        pass

    def pass1_cmd(self):
        convert_pass1_cmd = ""
        convert_pass1_cmd += "ffmpeg -i " + self.video_file
        convert_pass1_cmd += " -vcodec "  + self.ffmpeg_vcodec
        convert_pass1_cmd += " -pix_fmt yuv420p "
        convert_pass1_cmd += " -acodec " + self.ffmpeg_acodec
        convert_pass2_cmd += " -sws_flags lanczos "
        convert_pass1_cmd += " -vf " + self.vf
        convert_pass1_cmd += " -pass 1 --passlogfile tmp/" + self.video_file + " -f flv "
        convert_pass1_cmd += " -f " + self.fps
        convert_pass1_cmd += " -threads 12 "
        convert_pass1_cmd += " -y /dev/null > /dev/null 2>&1"
        return convert_pass1_cmd

    def pass2_cmd(self):
        convert_pass2_cmd = ""
        convert_pass2_cmd += "ffmpeg -i " + self.video_file
        convert_pass2_cmd += " -vcodec "  + self.ffmpeg_vcodec
        convert_pass2_cmd += " -pix_fmt yuv420p "
        convert_pass2_cmd += " -acodec " + self.ffmpeg_acodec
        convert_pass2_cmd += " -sws_flags lanczos "
        convert_pass2_cmd += " -vf " + self.vf
        convert_pass2_cmd += " -pass 1 --passlogfile tmp/" + self.video_file + " -f flv "
        convert_pass2_cmd += " -f " + self.fps
        convert_pass2_cmd += " -threads 12 "
        convert_pass2_cmd += " -y " + self.output_file + " > /dev/null 2>&1"
        return convert_pass2_cmd

    def command_execute(self):
        pass1_cmd = self.pass1_cmd1()
        pass2_cmd = self.pass2_cmd2()
        ret = subprocess.check_output(pass1_cmd, shell=True)
        if ret == 1:
            print("cmd pass1 %s failed" % (pass1_cmd))
            return
        ret = subprocess.check_output(pass2_cmd, shell=True)
        if ret == 1:
            print("cmd pass2 %s failed" % (pass2_cmd))
            return
        print("video_file: %s convert success" % (self.video_file))


if __name__ == "__main__":
    t = TranscodeOriginFile(
            configfile = './conf/transcode_origin_file.conf',
            video_type = 'default',
            resolution = 'SD',)
    t.command_execute()
