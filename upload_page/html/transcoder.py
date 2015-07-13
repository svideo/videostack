#!/usr/bin/env python
import hashlib
import configparser
import os
import sys
import re
#import upload
import select
import subprocess
import io

class Transcoder:
    def handle_body(self, name, body):
        if name == b'video_id':
            #self.init_write_handler(body)
            self.init_popen_handler();
        elif(name == b'upload'):
            #print(body)
            self.run_cmd_async(body)
            #self.write_handler.write(body)

    def read_conf(self):
        configfile = 'conf/transcoder.conf'
        if not os.path.exists(configfile):
            print("no config file")
            sys.exit(1)
        config = configparser.ConfigParser()
        config.read(configfile)

        return config

    def target_filename(self, video_id):
        config = self.read_conf()
        basedir = config['storage']['dir']

        m = hashlib.md5()
        m.update(video_id)
        md5_filename_str = m.hexdigest()
        print(video_id.decode())

        dir1 = md5_filename_str[:2]
        dir2 = md5_filename_str[2:4]
        target_dir = basedir + '/' + dir1 + '/' + dir2
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_filename = target_dir + '/' + md5_filename_str
        print(target_filename)
        return target_filename

    def init_write_handler(self,video_id):
        target_filename = self.target_filename(video_id)
        f = open(target_filename, mode='ab')
        self.write_handler = f

    def init_popen_handler(self):
        cmd = self.build_cmd()
        print(cmd)
        p = subprocess.Popen(cmd, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.stdout = p.stdout
        self.stdin  = p.stdin
        self.poll = p.poll()
        return

    def run_cmd_async(self, body):

        print(self.poll)
        if self.poll is not None:
            print("poll is not None")
            return
        self.stdin.write(body)

        while True:
            readable, writeable, exceptional = select.select([self.stdout], [], [], 0.1)
            if self.stdout in readable:
                line = self.stdout.read(1024).decode()
                print(line)
            else:
                print("break down readable")
                break

            #line = self.stdout.read(1024).decode()
            #print(line)
        #try:
        #    readable,writeable,exceptional = select.select([self.stdout], stdin_input, [], 0.5)
        #except:
        #    print("select error")
        #    sys.exit(1)

        #if self.stdin in writeable:
        #    print("write body")
        #    print(len(body))
        #    self.stdin.write(body)

        #if self.stdout in readable:
        #    print("in stdout")
        #    self.stdout.flush()
        #    stdoutLine = self.stdout.read(40960).decode()
        #    print(stdoutLine)

        #return

    def build_cmd(self):
        cmd = ""
        cmd += "ffmpeg -i - -vcodec copy -acodec copy -f flv -y /tmp/xxoo.flv 2>&1"
        #cmd = 'ffmpeg -i - -c:v libx264 -x264opts crf=31:ssim -an -f flv -y /dev/null -f rawvideo -y /dev/null 2>&1'
        if cmd is not None:
            self.cmd = cmd
        else:
            self.cmd = ""
        return cmd



#if __name__ == "__main__":
#    try:
#        s = upload.ForkingHTTPServer(("0.0.0.0", 80), upload.MyServer)
#        s.serve_forever()
#    except KeyboardInterrupt:
#        s.socket.close()
