API Reference
============================
### /interface/add\_staff\_ip
#### 描述
    添加staff转码机ip地址
#### 参数
    ip   : 字符串类型
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/add_staff_ip?ip=192.168.1.100

### /interface/update\_staff\_monitor
#### 描述
    更新staff转码机monitor
#### 参数
    ip            : staff转码机ip地址
    process_count : staff转码机进程数
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/update_staff_load?ip=192.168.1.100&process_count=1

### /interface/get\_video\_id
#### 描述
    生成video id、转码机ip地址
#### 参数

#### 返回值
    json格式返回video id、转码机ip地址
    video_id : 视频唯一标识
    ip       : 转码机ip地址
#### 示例
    /interface/get_video_id

### /interface/get\_video\_info
#### 描述
    获取视频信息,包括状态、截图总数、转码机ip地址、码率
#### 参数
    video_id : 视频唯一标识
#### 返回值
    json格式返回视频状态、截图总数、转码机ip、码率
    video_status : 视频状态,分别为success、failed、proceed
    snap_count   : 视频截图总数 
    ip           : 转码机ip地址
    bitrates     : uuid转码视频码率,支持多码率,用','分隔
#### 示例
    /interface/get_video_info?video_id=ytE3V3GyJigi2sqeBK

### /interface/update\_video\_status
#### 描述
    设置视频转码状态
#### 参数
    video_id : 视频唯一标识
    status   : 视频转码状态，分别为success、failed、proceed, 设置为proceed时需要加上bitrate参数
    bitrate  : 转码视频码率, status为proceed时传入此参数，其他状态不需要
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/update_video_status?video_id=ytwQrjkUBWi0u0syEC&status=success

### /interface/update\_video\_snap\_image\_count
#### 描述
    更新视频截图数量
#### 参数
    video_id         : 视频唯一标识
    snap_image_count : 视频截图总数
#### 返回值
    json格式返回操作状态以及失败原因
    status  : success、failed
    message : 失败原因
#### 示例
    /interface/update_video_snap_image_count?video_id=ytwQrjkUBWi0u0syEC&snap_image_count=100

### /interface/get\_video\_new\_snap\_image
#### 描述
    获取视频最新截图地址
#### 参数
    video_id : 视频唯一标识
#### 返回值
    json格式返回截图地址以及操作状态、失败原因
    status    : success、failed
    message   : 失败原因
    image_url : 截图地址 
#### 示例
    /interface/get_video_new_snap_image?video_id=ytE3V3GyJigi2sqeBK

### /interface/add\_video\_segment
#### 描述
    添加切片信息到x100speed_sortedset_videoid_bitrate
#### 参数
    video_id     : 视频唯一标识
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
    /interface/add_video_segment?video_id=ytwQrjkUBWi0u0syEC&bitrate=200&fragment_id=1&hostname=http://x100speed.com&storage_path=/ZH/CN/ereoimdfmdnndfdkd_200_1.ts&create_time=1349827788&fps=25&frame_count=250&file_size=3430

### /interface/\<play\_url\>.m3u8
#### 描述
    视频hls播放列表，“<play_url>”为视频video_id
#### 参数

#### 返回值
    返回多码率m3u8地址或空
#### 示例
    /interface/ytMVnxVFWEocSiWlNe.m3u8



















