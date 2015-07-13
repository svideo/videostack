#!/usr/bin/env python

cmd = ""
cmd += "ffmpeg -v verbose -i -"
cmd += " -vcodec libx264 -acodec copy "
cmd += " -f segment"
cmd += " -segment_format mpegts -segment_time 15"
cmd += " -y 2_%06d.ts"
print(cmd)
