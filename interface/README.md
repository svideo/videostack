x100speed_transcode 接口文档
============================
### /interface/staff\_ip\_add
#### 描述
    添加staff转码机ip地址
#### 参数
    ip   : staff转码机ip
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/staff_ip_add?ip=192.168.1.100

### /interface/staff\_load\_set
#### 描述
    设置staff转码机load值,新添加staff转码机默认load值为100
#### 参数
    load : staff转码机负载值
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/staff_load_set?load=60

### /interface/video\_uuid\_get
#### 描述
    生成全球唯一18位id以及返回video转码机ip地址
#### 参数

#### 返回值
    json格式返回18位长度uuid字符串、转码机ip地址
    uuid : 18位全球唯一id
    ip   : 转码机ip地址
#### 示例
    /interface/video_uuid_get

### /interface/video\_uuid\_info\_get
#### 描述
    获取uuid信息,包括状态、截图总数、转码机ip地址、码率
#### 参数
    uuid : 视频唯一标识
#### 返回值
    json格式返回uuid状态、截图总数、转码机ip、码率
    status     : uuid状态,分别为success、failed、proceed
    snap_count : 视频截图总数 
    ip         : 转码机ip地址
    bitrates   : uuid转码视频码率,支持多码率,用','分隔
#### 示例
    /interface/video_uuid_info_get?uuid=ytE3V3GyJigi2sqeBK

### /interface/video\_uuid\_status\_set
#### 描述
    设置视频转码状态
#### 参数
    uuid    : 视频唯一标识
    status  : 视频转码状态，分别为success、failed、proceed, 设置为proceed时需要加上bitrate参数
    bitrate : 转码视频码率, status为proceed时传入此参数，其他状态不需要
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/video_uuid_status_set?uuid=ytwQrjkUBWi0u0syEC&status=success

### /interface/video\_uuid\_snap\_count\_set
#### 描述
    设置视频截图数量
#### 参数
    uuid       : 视频唯一标识
    snap_count : 视频截图总数
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/video_uuid_snap_count_set?uuid=ytwQrjkUBWi0u0syEC&snap_count=100

### /interface/video\_uuid\_new\_image\_get
#### 描述
    获取uuid视频最新截图地址
#### 参数
    uuid : 视频唯一标识
#### 返回值
    json格式返回截图地址以及操作状态、失败原因
    status    : success、failed
    message   : 失败原因
    image_url : 截图地址 
#### 示例
    /interface/video_uuid_new_image_get?uuid=ytE3V3GyJigi2sqeBK

### /interface/video\_uuid\_segment\_add
#### 描述
    添加切片信息到x100speed_sortedset_uuid_bitrate
#### 参数
    uuid         : 视频唯一标识
    bitrate      : 视频码率
    fragment_id  : 切片序号
    hostname     : 视频存储主机名
    storage_path : 视频存储路径
    create_time  : 切片文件创建时间
    fps          : 视频帧率
    frame_count  : 视频帧数
    file_size    : 切片文件大小
#### 返回值
    json格式返回操作状态以及失败原因
    status : success、failed
    message : 失败原因
#### 示例
    /interface/video_uuid_segment_add?uuid=ytwQrjkUBWi0u0syEC&bitrate=200&fragment_id=1&hostname=http://x100speed.com&storage_path=/ZH/CN/ereoimdfmdnndfdkd_200_1.ts&create_time=1349827788&fps=25&frame_count=250&file_size=3430

### /interface/<play_url>.m3u8
#### 描述
    视频uuid的hls播放列表，“<play_url>”为视频uuid
#### 参数

#### 返回值
    返回多码率m3u8地址或空
#### 示例
    /interface/ytMVnxVFWEocSiWlNe.m3u8



















