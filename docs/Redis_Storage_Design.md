<!--
# author : Ren Peng
# github : https://github.com/svideo/x100speed_transcode.git
# description : Redis Storage Design
# date : 2015-08-17
-->

Redis Storage Design
=======================================

### x100speed\_hash\_videoid
#### 描述
    Hash数据结构存储视频转码状态、截图数量
    key : x100speed_hash_videoid
    field : 视频唯一标识video id
    value : 以|分割(status|image_count|ip|bitrate)，status表示视频转码状态（success、failed、proceed），image_count表示视频截图数量，ip为转码机地址, bitrate为视频码率，多个码率用","隔开
#### 数据结构
| Describe   | Data Structure | Key                      | Field              | Value                                       |
| ---------- |:--------------:|:------------------------:|:------------------:|:-------------------------------------------:|
| field name | hash           | x100speed\_hash\_videoid | videoid            |  status\|image_count\|ip\|bitrate1,bitrate2 |
| example    | hash           | x100speed\_hash\_videoid | ytmaWHUzDikIGwOLl6 |  success\|150\|10.209.79.229\|200,400       |

#### 操作
    更新转码状态、截图数量、ip地址、码率
    HSET x100speed_hash_videoid ytmaWHUzDikIGwOLl6 success|150|10.209.79.229|200,400

### x100speed\_sortedset\_videoid\_bitrate
#### 描述
    Sorted Set数据结构存储视频切片信息,videoid为视频唯一标识，bitrate为转码后的视频码率
    key : x100speed_sortedset_videoid_bitrate
    score : create_time(切片文件创建时间)
    member : 以字符串类型存储fragment_id|hostname|storage_path|create_time|fps|frame_count|file_size
#### 数据结构
| Describe   | Data Structure | Key                                    | score       | member               |
| ---------- |:--------------:|:--------------------------------------:|:-----------:|:--------------------:|
| field name | sorted set     | x100speed\_sortedset\_videoid\_bitrate | create_time | fragment\_id\|hostname\|storage\_path\|create\_time\|fps\|frame\_count\|file\_size |
| example    | sorted set     | x100speed\_sortedset\_videoid\_bitrate | 1437028427  | ytmaWHUzDikIGwOLl6\|http://x100speed.com\|/WH/DK/ytmaWHUzDikIGwOLl6\_1437028427\_cif.ts\|1437028427\|25\|250\|28427|

#### 操作
    添加切片信息
    ZADD x100speed_sortedset_videoid_bitrate 1437028427 ytmaWHUzDikIGwOLl6|http://x100speed.com|/WH/DK/ytmaWHUzDikIGwOLl6_1437028427_cif.ts|1437028427|25|250|28427

### x100speed\_hash\_staff
#### 描述
    使用hash结构存储staff转码机ip地址、process_count。ip数据类型为字符串，process_count数据类型整数以字符串形式保存
| Describe   | Data Structure | Key                    | Field         | Value            |
| ---------- |:--------------:|:----------------------:|:-------------:|:----------------:|
| field name | hash           | x100speed\_hash\_staff | ip            | process_count    |
| example    | hash           | x100speed\_hash\_staff | 192.168.1.100 | 0                |

#### 操作
    添加staff主机
    HSET x100speed_hash_staff 192.168.1.100 0
    
    更新staff主机load
    HSET x100speed_hash_staff 192.168.1.100 1

### x100speed\_ip\_list
#### 描述
    使用list结构存储转码机(ip)对应待转多个清晰度的videoid
| Describe   | Data Structure | Key                        | Value              |
| ---------- |:--------------:|:--------------------------:|:------------------:|
| field name | list           | x100speed\_ip\_list        | videoid            |
| example    | list           | x100speed\_10.0.2.15\_list | yxzpnmliogGqG2cADk |

#### 操作
    添加待转多清晰度videoid
    RPUSH x100speed_10.0.2.15_list yxzpnmliogGqG2cADk
    
