from x100http import X100HTTP, X100Response
import time, redis, x100idgen, hashlib

def add_staff_ip(request):
    ip            = request.get_arg('ip')
    process_count = 100
    response      = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
          
    if not ip:
        response.set_body('{"status":"failed", "message":"ip empty"}')
        return response
    
    r = redis_connect()
    r.hset('x100speed_hash_staff', ip, process_count)

    response.set_body('{"status":"success", "message":""}')
    return response

def update_staff_monitor(request):
    ip            = request.get_arg('ip')
    process_count = request.get_arg('process_count') 
    response      = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    if not ip or not process_count:
        response.set_body('{"status":"failed", "message":"ip or process_count empty"}')
        return response

    r = redis_connect()
    r.hset('x100speed_hash_staff', ip, process_count)

    response.set_body('{"status":"success", "message":""}')
    return response

def get_video_id(request):
    ip          = ""
    userAgent   = request.get_header('User-Agent')
    millisecond = int(round(time.time() * 1000))
    ip          = request.get_remote_ip()
    response    = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    r           = redis_connect()
    staff_list  = r.hgetall('x100speed_hash_staff') 
    if not staff_list:
        response.set_body('{"status":"failed", "message":"staff ip empty"}')
        return response

    idle_staff_list = {key: value for key, value in staff_list.items() if int(value) <= 0}    
    if not idle_staff_list:
        response.set_body('{"status":"failed", "message":"staff is busying"}')
        return response
    
    staff       = idle_staff_list.popitem()
    staff_ip    = staff[0].decode()
    hash_string = ip + userAgent + str(millisecond)
    idgen       = x100idgen.IdGen()
    video_id    = idgen.gen_id(hash_string)
    infor       = '{"video_id":"' + video_id + '","ip":"' + staff_ip + '"}'
    
    response.set_body(infor)

    return response

def update_video_status(request):
    video_id = request.get_arg('video_id')
    status   = request.get_arg('status')
    ip       = request.get_remote_ip()
    response = X100Response()
    
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    if not video_id or not status:
        response.set_body('{"status":"failed", "message":"video_id or status empty"}')
        return response

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_videoid", video_id)
    if not ret:
        if status == "proceed":
            bitrate = request.get_arg('bitrate')
            if not bitrate:
                response.set_body('{"status":"failed", "message":"proceed first bitrate empty"}')
                return response

            value = status + '|' + '|' + ip + '|' + bitrate
            r.hset('x100speed_hash_videoid', video_id, value)
            response.set_body('{"status":"success", "message":""}')
        else:
            response.set_body('{"status":"failed", "message":"redis not have video_id"}')
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
            bitrate = request.get_arg('bitrate')
            if not bitrate:
                response.set_body('{"status":"failed", "message":"bitrate params is empty"}')
                return response

            ret = video_bitrate_add(video_id, bitrate)
            if ret:
                value += '|' + ret
            else:
                value += '|' + bitrate
        else:
            value += '|' + item

    r.hset('x100speed_hash_videoid', video_id, value)

    response.set_body('{"status":"success", "message":""}')
    return response

def video_bitrate_add(video_id, bitrate):
    if not video_id or not bitrate:
        return ""

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_videoid", video_id)
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

def update_video_snap_image_count(request):
    video_id         = request.get_arg('video_id')
    snap_image_count = request.get_arg('snap_image_count')
    response         = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    if not video_id or not snap_image_count:
        response.set_body('{"status":"failed", "message":"video_id or snap_image_count empty"}')
        return response

    value = ''
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_videoid", video_id)
    if not ret:
        response.set_body('{"status":"failed", "message":"redis not have video_id"}')
        return response
    
    infor            = ret.decode()
    string_split     = infor.split('|')
    string_split_len = len(string_split)

    for index, item in enumerate(string_split):
        if index == 0:
            value += item
        elif index == 1:
            value += '|' + snap_image_count
        else :
           value += '|' + item

    r.hset('x100speed_hash_videoid', video_id, value)

    response.set_body('{"status":"success", "message":""}')
    return response

def get_video_new_snap_image(request):
    video_id = request.get_arg('video_id')
    response = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    if not video_id:
        response.set_body('{"status":"failed", "message":"video_id empty"}')
        return response
    
    r     = redis_connect()
    ret   = r.hget("x100speed_hash_videoid", video_id)
    if not ret:
        response.set_body('{"status":"failed", "message":"redis not have video_id"}')
        return response    

    infor         = ret.decode()
    string_split  = infor.split('|')
    snap_count    = string_split[1]
    ip            = string_split[2]
    source_string = video_id + '_' + snap_count + '.jpg'
    string_hash   = hashlib.new("md5", source_string.encode()).hexdigest()
    dir_first     = string_hash[:3]
    dir_second    = string_hash[3:6]
    dir_third     = string_hash[6:9]
    image_url     = 'http://' + ip + '/' + dir_first + '/' + dir_second + '/' + dir_third + '/' +  video_id + '_' + snap_count + '.jpg'

    response.set_body('{"status":"success", "message":"", "image_url":"' + image_url + '"}')
    return response

def add_video_segment(request):
    video_id     = request.get_arg('video_id')
    bitrate      = request.get_arg('bitrate')
    fragment_id  = request.get_arg('fragment_id')
    hostname     = request.get_arg('hostname')
    storage_path = request.get_arg('storage_path') 
    create_time  = request.get_arg('create_time')
    fps          = request.get_arg('fps')
    frame_count  = request.get_arg('frame_count')
    file_size    = request.get_arg('file_size')
    response     = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")

    if not video_id or not fragment_id or not hostname or not storage_path \
       or not create_time or not fps or not frame_count or not file_size:
        response.set_body('{"status":"failed", "message":"params have error"}')
        return response
    
    sorted_set_key    = 'x100speed_sortedset_' + video_id + '_' + bitrate
    sorted_set_score  = create_time
    sorted_set_member = fragment_id + '|' + hostname + '|' + storage_path + '|' + create_time \
                        + '|' + fps + '|' + frame_count + '|' + file_size
    r   = redis_connect()
    ret = r.zadd(sorted_set_key, sorted_set_score, sorted_set_member)

    response.set_body('{"status":"success", "message":""}')
    return response


def get_video_info(request):
    video_id = request.get_arg('video_id')
    response = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    
    if not video_id:
        response.set_body('{"status":"failed", "message":"video_id empty"}')
        return response

    r   = redis_connect()
    ret = r.hget("x100speed_hash_videoid", video_id)
    if not ret:
        response.set_body('{"status":"failed", "message":"redis not have video_id"}')
        return response

    infor        = ret.decode()
    string_split = infor.split('|')
    value        = '{"status":"' + string_split[0] + '", "snap_img_count":"' + string_split[1]\
                    + '", "ip":"' + string_split[2] + '", "bitrates":"' + string_split[3] + '"}'

    response.set_body(value)
    return response

def video_play(request):
    video_id = request.get_arg("play_url")
    response = X100Response()

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    response.set_header("Content-Type", "application/vnd.apple.mpegurl")

    r   = redis_connect()
    ret = r.hget('x100speed_hash_videoid', video_id)
    if not ret:
        response.set_body("")
        return response

    video_info      = ret.decode()
    video_info_list = video_info.split('|')

    if video_info_list[0] == "failed":
        response.data = ""
        return response

    ip            = video_info_list[2]
    bitrates      = video_info_list[3]
    bitrates_list = bitrates.split(',')
    
    m3u8_value = '#EXTM3U\n'
    for bitrate in bitrates_list:
        total_bitrate = int(bitrate) * 1024
        m3u8_value   += '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=' + str(total_bitrate) + '\n'
        m3u8_value   += 'http://10.221.193.64/interface/' + video_id + '_' + bitrate + '.m3u8\n'

    response.set_body(m3u8_value)
    return response

def video_play_child(request):
    video_id = request.get_arg("play_url")
    bitrate  = request.get_arg("play_bitrate")
    response = X100Response()
    
    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET")
    response.set_header("Content-Type", "application/vnd.apple.mpegurl")

    r   = redis_connect()
    ret = r.hget('x100speed_hash_videoid', video_id)
    if not ret:
        response.set_body("")
        return response

    video_info      = ret.decode()
    video_info_list = video_info.split('|')
    play_type       = "live"
    if video_info_list[0] == "success":
        play_type = "vod"
    elif video_info_list[0] == "failed":
        response.data = ""
        return response

    video_sortedset = 'x100speed_sortedset_' + video_id + '_' + str(bitrate)
    fragment_list   = ""

    if play_type == "live":
        fragment_list = r.zrange(video_sortedset, -3, -1)
    elif play_type == "vod":
        fragment_list = r.zrange(video_sortedset, 0, -1)
    
    if not fragment_list:
        response.set_body("")
        return response

    video_m3u8            = ""
    video_m3u8_tmp        = ""
    video_m3u8_sequence   = ""
    max_fragment_duration = 0.000
    
    for fragment in fragment_list:
        fragment_string = fragment.decode()
        fragment_array  = fragment_string.split('|')
        
        if not video_m3u8_sequence:
            video_m3u8_sequence = str(fragment_array[0])
 
        fragment_duration = round(int(fragment_array[5]) / int(fragment_array[4]), 3)
        if fragment_duration > max_fragment_duration:
            max_fragment_duration = fragment_duration

        fragment_url  = fragment_array[1] + fragment_array[2]
        video_m3u8_tmp += '#EXTINF:' + str(fragment_duration)
        video_m3u8_tmp += "\n"
        video_m3u8_tmp += fragment_url
        video_m3u8_tmp += "\n"
    
    video_m3u8 += "#EXTM3U\n"
    video_m3u8 += "#EXT-X-VERSION:5\n"
    video_m3u8 += "#EXT-X-TARGETDURATION:" + str(max_fragment_duration) + "\n"
    video_m3u8 += "#EXT-X-MEDIA-SEQUENCE:" + video_m3u8_sequence + "\n"
    video_m3u8 += "#EXT-X-ALLOW-CACHE:YES\n"
    video_m3u8 += video_m3u8_tmp

    if play_type == "vod":
        video_m3u8 += "#EXT-X-ENDLIST\n"
    
    response.set_body(video_m3u8)
    return response

def redis_connect():
    host='127.0.0.1'
    port=6379
    db=0
    password='foobared'

    r = redis.StrictRedis(host = host, port = port, password = password, db = db)
    return r


