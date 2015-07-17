from flask import Flask,make_response
import time
app = Flask(__name__)

segment_time = 10
segment_count = 3

def get_vod_segment_list():
    return [1, 2, 3]

def get_live_segment_list():
    ts = int(time.time())
    mod = ts % (segment_time * segment_count)
    segment_list = []
    if mod >= 0 and mod <= segment_time:
        segment_list = [1, 2, 3]
    elif mod >= segment_time and mod <= segment_time * 2:
        segment_list = [2, 3, 1]
    elif mod >= segment_time * 2 and mod <= segment_time * 3:
        segment_list = [3, 1, 2]
    return segment_list

def get_m3u8_start_vod():
    m3u8_start  = "#EXT-X-VERSION:3\n"
    m3u8_start += "#EXT-X-MEDIA-SEQUENCE:0\n"
    m3u8_start += "#EXT-X-TARGETDURATION:" + str(segment_time+1) + "\n"
    return m3u8_start

def get_m3u8_end_vod():
    return "#EXT-X-ENDLIST\n"

def get_m3u8_start_live():
    ts = int(time.time())
    mod = ts % 100000
    sequence = int( ( ts % 100000 ) / 10 )

    m3u8_start  = "#EXT-X-VERSION:3\n"
    m3u8_start += "#EXT-X-MEDIA-SEQUENCE:" + str(sequence) + "\n"
    m3u8_start += "#EXT-X-TARGETDURATION:" + str(segment_time+1) + "\n"
    return m3u8_start

@app.route('/vod.m3u8')
def vod_m3u8():
    response = make_response()
    response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    result = get_m3u8_start_vod()
    for segment_numer in get_vod_segment_list():
        result += "#EXTINF:" + str(segment_time)
        result += "\n"
        result += "2015070021_cif_00000" + str(segment_numer) + ".ts"
        result += "\n"
    result += get_m3u8_end_vod()
    response.data = result
    return response

@app.route('/live.m3u8')
def live_m3u8():
    response = make_response()
    response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    result = get_m3u8_start_live()
    for segment_numer in get_live_segment_list():
        result += "#EXTINF:" + str(segment_time)
        result += "\n"
        result += "2015070021_cif_00000" + str(segment_numer) + ".ts"
        result += "\n"
    response.data = result
    return response

@app.route('/<filename>.ts')
def tsfile(filename):
    response = make_response()
    response.headers['Content-Type'] = 'video/MP2T'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    response.data = open(filename + ".ts").read()
    return response

if __name__ == '__main__':
    #app.debug = True
    app.run(host="0.0.0.0", threaded=True)
