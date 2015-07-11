#!/usr/bin/env python
import hashlib
import configparser
import os
import sys
import re

class Transcoder:
    def handle_body(self, name, body):
        if name == b'channel_id':
            m = hashlib.md5()
            m.update(body)
            md5_filename_str = m.hexdigest()

            target_filename = self.target_filename(md5_filename_str)
            f = open(target_filename, mode='ab')
            self.filehandle = f
        else:
            self.filehandle.write(body)

    def read_conf(self):
        configfile = 'conf/transcoder.conf'
        if not os.path.exists(configfile):
            print("no config file")
            sys.exit(1)
        config = configparser.ConfigParser()
        config.read('conf/transcoder.conf')

        return config

    def target_filename(self, filename):
        config = self.read_conf()
        basedir = config['storage']['dir']

        regex_file = re.search('(\w{2})(\w{2})', filename)
        if regex_file:
            dir1 = regex_file.group(1)
            dir2 = regex_file.group(2)

        target_dir = basedir + '/' + dir1 + '/' + dir2
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_filename = target_dir + '/' + filename
        return target_filename
