#!/usr/bin/env pytnon3

import unittest
from unittest import TestCase
import sys
sys.path.append("../")
from transcoder import Transcoder
from x100utils.x100util import *
from x100utils.x100config import load_config

class TestMethods(unittest.TestCase):

    #transcoder = Transcoder()
    def setUp(self):
        self.ts_file = 'data/test.ts'
        self.flv_file = 'data/test.flv'
        self.maxDiff = None

    def test_md5(self):
        (ts_dir, ts_filename) = self.ts_file.split('/')
        expected_md5_string = '9d878e6c8076c7cdd71130118d1fc802'
        md5_string = md5(ts_filename)
        self.assertEqual(expected_md5_string, md5_string)

    def test_load_conf(self):
        config_ob = load_config('../conf/transcoder.conf')
        self.assertIsNotNone(config_ob)

    def test_request_info_serialize(self):
        expected_info = ['a=hello&b=world&', 'b=world&a=hello&']
        info = request_info_serialize(a='hello', b='world')
        self.assertIn(info, expected_info)

    def test_get_target_file(self):
        config = load_config('../conf/transcoder.conf')
        release_dir = config['storage']['release_dir']
        (ts_dir, ts_filename) = self.ts_file.split('/')
        filetype = 'ts'
        (a, b) = get_target_file(release_dir, ts_filename, filetype)
        self.assertEqual( get_target_file(release_dir, ts_filename, filetype),
                           ('/data1/hls/segment/ts/9d8/78e/6c8/test.ts', '/ts/9d8/78e/6c8/test.ts'))

    #def test_build_cmd(self):
    #    config = load_config('../conf/transcoder.conf')
    #    expected_ffmpeg_cmd = 'ffmpeg -v verbose -i - -filter_complex " [0:v:0]fps=15,scale=352:288,split=2[voutA][vtmpB], [vtmpB]fps=0.5,scale=176:144[voutB],[0:a:0]asplit=1[aoutA]"  -map [voutA] -map [aoutA] -c:v libx264 -x264opts bitrate=450:no-8x8dct:bframes=0:no-cabac:weightp=0:no-mbtree:me=dia:no-mixed-refs:partitions=i8x8,i4x4:rc-lookahead=0:ref=1:subme=1:trellis=0 -c:a libfdk_aac -profile:a aac_he -b:a 16k-f segment -segment_format flv -segment_time 10 -y /tmp/hls/segment/abc_%d.flv -map [voutB] -y /tmp/hls/segment/abc_%d.jpg 2>&1'
    #    ffmpeg_cmd = build_cmd('abc', config)
    #    self.assertEqual(expected_ffmpeg_cmd, ffmpeg_cmd, 'why not equal')


if __name__ == "__main__":
    unittest.main()
