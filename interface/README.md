x100speed_transcode 接口文档
============================

### /interface/video\_uuid\_get
#### 描述
    id生成器，可生成全球唯一18位id
#### 参数

#### 返回值
    返回18位长度uuid字符串
#### 示例
    http://10.221.193.196:5000/interface/video_uuid_get

### /interface/video\_uuid\_status\_set
#### 描述
    设置视频转码状态
#### 参数
    uuid   : 视频唯一标识
    status : 视频转码状态，分别为success、failed、proceed
#### 返回值
    status  : success、failed
    message : 失败原因
    示例
        {"status":"success", "message":""}
        {"status":"failed",  "message":"uuid is empty"}
#### 示例
    http://10.221.193.196:5000/interface/video_uuid_status_set?uuid=ytwQrjkUBWi0u0syEC&status=success

### /interface/video\_uuid\_snap\_count\_set
#### 描述
    设置视频截图数量
#### 参数
    uuid       : 视频唯一标识
    snap_count : 视频截图总数
#### 返回值
    status  : success、failed
    message : 失败原因
    示例
        {"status":"success", "message":""}
        {"status":"failed",  "message":"uuid is empty"}

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
    status : success、failed
    message : 失败原因
    示例
        {"status":"success", "message":""}
        {"status":"failed",  "message":"params error"}
#### 示例
    http://10.221.193.196:5000/interface/video_uuid_segment_add?uuid=ytwQrjkUBWi0u0syEC&bitrate=200&fragment_id=1&hostname=http://x100speed.com&storage_path=/ZH/CN/ereoimdfmdnndfdkd_200_1.ts&create_time=1349827788&fps=25&frame_count=250&file_size=3430

















