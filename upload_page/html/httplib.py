#!/usr/bin/env python
#coding=utf8

import urllib
import http.client

def segment_add(host, url, args):
    request_url = url + '?' + args
    print(request_url)
    conn = http.client.HTTPConnection(host, 80, timeout=10)
    conn.request("GET", url)
    res = conn.getresponse()
    status = res.status
    print(status)
    print(res.read())


#args = "uuid=b1946ac92492d2347c6235b4d2611184&storage_path=/9ea/ccf/da5/b1946ac92492d2347c6235b4d2611184_000001.flv&fps=25&create_time=1437120063&file_size=153556&hostname=http://www.x100speed.com&bitrate=105K48KK&frame_count=250&"
args = "a=1&b=2"
#d = {'a' : 1, 'b' :2}
#args = urllib.urlencode(d)
#print(args)
segment_add('www.b.com', '/echo.php', args)

