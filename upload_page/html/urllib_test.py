#import urllib.request
#
#f = urllib.request.urlopen('http://www.b.com/echo.php')
#print(f.read().decode('utf-8'))

#import urllib.request
#import urllib.parse
#data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
#data = data.encode('utf-8')
#request = urllib.request.Request("http://www.b.com/echo.php")
## adding charset parameter to the Content-Type header.
##request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
#with urllib.request.urlopen(request, data) as f:
#    print(f.read().decode('utf-8'))

import urllib.request
import json
args = "fragment_id=1&uuid=b1946ac92492d2347c6235b4d2611184&storage_path=/9ea/ccf/da5/b1946ac92492d2347c6235b4d2611184_000001.flv&fps=25&create_time=1437120063&file_size=153556&hostname=http://www.x100speed.com&bitrate=105K48KK&frame_count=250"
d = {}
for kv in args.split('&'):
    key , value = kv.split('=')
    d[key] = value

url = "http://10.221.193.196:5000/interface/video_uuid_segment_add?" + args

#data = urllib.parse.urlencode(d)
#data = data.encode('utf-8')
def http_request(url, args):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as f:
        return f.read().decode('utf-8')

res = http_request(url, args)
o = json.loads(res)
print(o['status'])
