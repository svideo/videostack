#!/usr/bin/env python

from mediainfo import MediaInfo

m = MediaInfo(filename = '/tmp/oooo.flv')

print(m.audio_codec)
