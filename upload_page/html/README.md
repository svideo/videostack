# upload_page

----------------------

## 描述

视频上传页面
 
## 运行server

### 转码工具检测

python upload.py

### 访问

http://ip/upload.html

## uuid md5 计算方式

echo -n 'ytOb5FJEYgmKU0epYq_2.jpg' | md5sum
108fce3dfaf0f3ff6267e8b2d262dba6

访问路径分三级目录, 每级目录顺序去md5 3 位:
http://hostname/108/fce/3df

