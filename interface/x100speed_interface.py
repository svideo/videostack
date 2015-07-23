from flask import Flask,request,make_response
import time,redis,x100idgen,hashlib

app = Flask(__name__)

@app.route("/interface/staff_ip_add")
def staff_ip_add():
    ip   = request.args.get('ip')
    load = 100

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    if not ip:
        response.data = '{"status":"failed", "message":"ip is null"}'
        return response
    
    r = redis_connect()
    r.hset('x100speed_hash_staff', ip, load)

    response.data = '{"status":"success", "message":""}'
    return response

@app.route("/interface/staff_load_set")
def staff_load_set():
    ip   = request.args.get('ip')
    load = request.args.get('load') 

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    if not ip or not load:
        response.data = '{"status":"failed", "message":"ip or load is null"}'
        return response

    r = redis_connect()
    r.hset('x100speed_hash_staff', ip, load)

    response.data = '{"status":"success", "message":""}'
    return response
    
@app.route("/interface/video_uuid_get")
def video_uuid_get():
    userAgent   = request.headers.get('User-Agent')
    ip          = request.remote_addr
    millisecond = int(round(time.time() * 1000))
 
    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    r           = redis_connect()
    staff_list  = r.hgetall('x100speed_hash_staff') 
    if not staff_list:
        response.data = '{"status":"failed", "message":"staff ip empty"}'
        return response

    idle_staff_list = {key: value for key, value in staff_list.items() if float(value) < 30}    
    if not idle_staff_list:
        response.data = '{"status":"failed", "message":"staff is busying"}'
        return response
    
    staff    = idle_staff_list.popitem()
    staff_ip = staff[0].decode()

    hash_string = ip + userAgent + str(millisecond)
    idgen       = x100idgen.IdGen()
    uuid        = idgen.gen_id(hash_string)
    
    infor = '{"uuid":"' + uuid + '","ip":"' + staff_ip + '"}'
    response.data = infor
    return response

@app.route("/interface/video_uuid_info_get")
def video_uuid_info_get():
    uuid = request.args.get('uuid')

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    if not uuid:
        response.data = '{"status":"failed", "message":"uuid params is empty"}'
        return response

    r   = redis_connect()
    ret = r.hget("x100speed_hash_uuid", uuid)
    if not ret:
        response.data = '{"status":"failed", "message":"redis not have uuid"}'
        return response

    infor        = ret.decode()
    string_split = infor.split('|')
    value        = '{"status":"' + string_split[0] + '", "snap_count":"' + string_split[1]\
                    + '", "ip":"' + string_split[2] + '", "bitrates":"' + string_split[3] + '"}'

    response.data = value
    return response

@app.route("/interface/video_uuid_status_set")
def video_uuid_status_set():
    uuid   = request.args.get('uuid')
    status = request.args.get('status')
    
    if not request.headers.getlist("X-Forwarded-Host"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-Host")[0]

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    if not uuid or not status:
        response.data = '{"status":"failed", "message":"uuid or status params is empty"}'
        return response

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_uuid", uuid)
    if not ret:
        if status == "proceed":
            bitrate = request.args.get('bitrate')
            if not bitrate:
                response.data = '{"status":"failed", "message":"proceed first bitrate params is empty"}'
                return response
            value = status + '|' + '|' + ip + '|' + bitrate
            r.hset('x100speed_hash_uuid', uuid, value)
            response.data = '{"status":"success", "message":""}'
        else:
            response.data = '{"status":"failed", "message":"redis not have uuid"}'
        return response
     
    infor        = ret.decode()
    string_split = infor.split('|')
    value        = status
    for index, item in enumerate(string_split):
        if index == 0:
            continue
        elif index == 2:
            value += '|' + ip
        elif index == 3 and status == "proceed":
            bitrate = request.args.get('bitrate')
            if not bitrate:
                response.data = '{"status":"failed", "message":"bitrate params is empty"}'
                return response

            ret = video_uuid_bitrate_add(uuid, bitrate)
            if ret:
                value += '|' + ret
            else:
                value += '|' + bitrate
        else:
            value += '|' + item

    r.hset('x100speed_hash_uuid', uuid, value)

    response.data = '{"status":"success", "message":""}'
    return response

def video_uuid_bitrate_add(uuid, bitrate):
    if not uuid or not bitrate:
        return ""

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_uuid", uuid)
    if not ret:
        return ""
    
    infor            = ret.decode()
    string_split     = infor.split('|')
    string_split_len = len(string_split)

    bitrates = string_split[3].split(',')
    bitrates.append(str(bitrate))
    bitrates = list(set(bitrates))
    bitrates.sort(key = int)
    value = ',' . join(bitrates)
    
    return value

@app.route("/interface/video_uuid_snap_count_set")
def video_uuid_snap_count_set():
    uuid       = request.args.get('uuid')
    snap_count = request.args.get('snap_count')

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    if not uuid or not snap_count:
        response.data = '{"status":"failed", "message":"uuid or snap_count params is empty"}'
        return response

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_uuid", uuid)
    if not ret:
        response.data = '{"status":"failed", "message":"redis not have uuid"}'
        return response
    
    infor            = ret.decode()
    string_split     = infor.split('|')
    string_split_len = len(string_split)

    for index, item in enumerate(string_split):
        if index == 0:
            value += item
        elif index == 1:
            value += '|' + snap_count
        else :
           value += '|' + item

    r.hset('x100speed_hash_uuid', uuid, value)

    response.data = '{"status":"success", "message":""}'
    return response

@app.route("/interface/video_uuid_new_image_get")
def video_uuid_new_image_get():
    uuid = request.args.get('uuid')
    
    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    if not uuid:
        response.data = '{"status":"failed", "message":"uuid params is empty"}'
        return response
    
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_uuid", uuid)
    if not ret:
        response.data = '{"status":"failed", "message":"redis not have uuid"}'
        return response    

    infor         = ret.decode()
    string_split  = infor.split('|')
    snap_count    = string_split[1]
    ip            = string_split[2]
    source_string = uuid + '_' + snap_count + '.jpg'
    string_hash   = hashlib.new("md5", source_string.encode()).hexdigest()
    dir_first     = string_hash[:3]
    dir_second    = string_hash[3:6]
    dir_third     = string_hash[6:9]
    image_url     = 'http://' + ip + '/' + dir_first + '/' + dir_second + '/' + dir_third + '/' +  uuid + '_' + snap_count + '.jpg'

    response.data = '{"status":"success", "message":"", "image_url":"' + image_url + '"}'
    return response

@app.route("/interface/video_uuid_segment_add")
def video_uuid_segment_add():
    uuid         = request.args.get('uuid')
    bitrate      = request.args.get('bitrate')
    fragment_id  = request.args.get('fragment_id')
    hostname     = request.args.get('hostname')
    storage_path = request.args.get('storage_path') 
    create_time  = request.args.get('create_time')
    fps          = request.args.get('fps')
    frame_count  = request.args.get('frame_count')
    file_size    = request.args.get('file_size')

    response  = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'

    if not uuid or not fragment_id or not hostname or not storage_path \
       or not create_time or not fps or not frame_count or not file_size:
        response.data = '{"status":"failed", "message":"params have error"}'
        return response
    
    sorted_set_key    = 'x100speed_sortedset_' + uuid + '_' + bitrate
    sorted_set_score  = create_time
    sorted_set_member = fragment_id + '|' + hostname + '|' + storage_path + '|' + create_time \
                        + '|' + fps + '|' + frame_count + '|' + file_size
    r   = redis_connect()
    ret = r.zadd(sorted_set_key, sorted_set_score, sorted_set_member)

    response.data = '{"status":"success", "message":""}'
    return response

@app.route("/interface/<play_url>.m3u8")
def video_uuid_play(play_url):
    uuid = play_url

    response = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'

    r   = redis_connect()
    ret = r.hget('x100speed_hash_uuid', uuid)
    if not ret:
        response.data = ""
        return response

    uuid_info      = ret.decode()
    uuid_info_list = uuid_info.split('|')
    play_type      = "live"
    if uuid_info_list[0] == "success":
        play_type = "vod"
    elif uuid_info_list[0] == "failed":
        response.data = ""
        return response

    ip            = uuid_info_list[2]
    bitrates      = uuid_info_list[3]
    bitrates_list = bitrates.split(',')
    
    m3u8_value = '#EXTM3U\n'
    for bitrate in bitrates_list:
        total_bitrate = int(bitrate) * 1024
        m3u8_value   += '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=' + str(total_bitrate) + '\n'
        m3u8_value   += 'http://10.221.193.64/interface/' + uuid + '_' + bitrate + '.m3u8\n'

    response.data = m3u8_value
    return response

@app.route("/interface/<play_url>_<int:play_bitrate>.m3u8")
def video_uuid_play_child(play_url, play_bitrate):
    uuid    = play_url
    bitrate = play_bitrate

    response = make_response()
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'

    r   = redis_connect()
    ret = r.hget('x100speed_hash_uuid', uuid)
    if not ret:
        response.data = ""
        return response

    uuid_info      = ret.decode()
    uuid_info_list = uuid_info.split('|')
    play_type      = "live"
    if uuid_info_list[0] == "success":
        play_type = "vod"
    elif uuid_info_list[0] == "failed":
        response.data = ""
        return response

    uuid_sortedset = 'x100speed_sortedset_' + uuid + '_' + str(bitrate)
    fragment_list  = ""

    if play_type == "live":
        fragment_list = r.zrange(uuid_sortedset, -3, -1)
    elif play_type == "vod":
        fragment_list = r.zrange(uuid_sortedset, 0, -1)
    
    if not fragment_list:
        response.data = ""
        return response

    uuid_m3u8             = ""
    uuid_m3u8_tmp         = ""
    uuid_m3u8_sequence    = ""
    max_fragment_duration = 0.000
    
    for fragment in fragment_list:
        fragment_string = fragment.decode()
        fragment_array  = fragment_string.split('|')
        
        if not uuid_m3u8_sequence:
            uuid_m3u8_sequence = str(fragment_array[0])
 
        fragment_duration = round(int(fragment_array[5]) / int(fragment_array[4]), 3)
        if fragment_duration > max_fragment_duration:
            max_fragment_duration = fragment_duration

        fragment_url  = fragment_array[1] + fragment_array[2]
        uuid_m3u8_tmp += '#EXTINF:' + str(fragment_duration)
        uuid_m3u8_tmp += "\n"
        uuid_m3u8_tmp += fragment_url
        uuid_m3u8_tmp += "\n"
    
    uuid_m3u8 += "#EXTM3U\n"
    uuid_m3u8 += "#EXT-X-VERSION:5\n"
    uuid_m3u8 += "#EXT-X-TARGETDURATION:" + str(max_fragment_duration) + "\n"
    uuid_m3u8 += "#EXT-X-MEDIA-SEQUENCE:" + uuid_m3u8_sequence + "\n"
    uuid_m3u8 += "#EXT-X-ALLOW-CACHE:YES\n"
    uuid_m3u8 += uuid_m3u8_tmp

    if play_type == "vod":
        uuid_m3u8 += "#EXT-X-ENDLIST\n"
    
    response.data = uuid_m3u8
    return response

def redis_connect():
    host='127.0.0.1'
    port=6379
    db=0
    password='foobared'

    r = redis.StrictRedis(host = host, port = port, password = password, db = db)
    return r

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
