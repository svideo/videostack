x100speed_transcode Redis 数据结构说明文档
=======================================

### video\_id\_max
#### 描述
    存储当前最大的视频id值，利用redis原子性INCR获取，数据类型为数字的字符串，初始值为1000000
#### 数据结构
| Key            | Value         | Type   |
| -------------- |:-------------:| ------:|
| video\_id\_max | 100000        | String |

#### 操作
    初始化
    SET video_id_max 100000

    增加Value
    INCR video_id_max

### video\_staff\_hash
#### 描述
    使用hash结构存储staff转码机ip地址、load。ip数据类型为字符串，load数据类型为浮点数以字符串形式保存
| Data Structure | Key                | Field         | Type   | Value   | Type   |
| -------------- |:------------------:|:-------------:|:------:|:-------:| ------:|
| hashes         | video\_staff\_hash | 192.168.1.100 | String | 90.5    | String |

#### 操作
    添加staff主机
    HSET staff_hash 192.168.1.100 0
    
    更新staff主机load
    HSET staff_hash 192.168.1.100 99.9
    