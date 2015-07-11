x100speed_transcode Redis 数据结构说明文档
=======================================

### video_id_max
#### 描述
    存储当前最大的视频id值，利用redis原子性INCR获取，数据类型为数字的字符串，初始值为1000000
#### 数据结构
| Key            | Value         | Type   |
| -------------- |:-------------:| ------:|
| video_id_max   | 100000        | String |

#### 操作
    初始化
    SET video_id_max 100000

    增加Value
    INCR video_id_max

