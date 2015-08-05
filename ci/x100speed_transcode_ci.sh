#!/usr/bin/env bash

# author : renpeng
# github : https://github.com/laodifang
# description : x100speed transcode ci
# date : 2015-08-05

INSTALL_PACKAGET_PATH='/data/install'

# python3
PYTHON3_URL='http://10.221.193.64:8000/Python-3.4.3.tgz'
PYTHON3_PACKET='Python-3.4.3.tgz'
PYTHON3_NAME='Python-3.4.3'
PYTHON3_BIN_PATH='/usr/local/bin/python3'

# ffmpeg
FFMPEG_URL='http://10.221.193.64:8000/ffmpeg_install_2.7.2.tar.gz'
FFMPEG_PACKET='ffmpeg_install_2.7.2.tar.gz'
FFMPEG_NAME='ffmpeg_install_2.7.2'
FFMPEG_BIN_PATH='/usr/bin/ffmpeg'

# redis
REDIS_URL=''
REDIS_PACKET=''
REDIS_NAME=''
REDIS_BIN_PATH='/usr/bin/redis-server'

# require python3 module
REQUIRE_PYTHON3_MODULE='redis x100http x100idgen x100daemon x100mpegts'
PIP3_SOURCE='http://mirrors.aliyun.com/pypi/simple'

# app
APP_PATH='/data'
X100SPEED_TRANSCODE_URL='http://10.221.193.64:8000/x100speed_transcode.tar.gz'
X100SPEED_TRANSCODE_PACKET='x100speed_transcode.tar.gz'
X100SPEED_TRANSCODE_NAME='x100speed_transcode'


# disable firewalld
sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo setenforce 0

# init server
sudo yum -y install epel-release git openssl openssl-devel perl-devel
sudo wget  http://xrl.us/cpanm --no-check-certificate -O /sbin/cpanm
sudo chmod +x  /sbin/cpanm

if [ ! -s '/sbin/cpanm' ]; then
    echo "!!!!!! cpanm install failed !!!!!!"
    exit 0
fi

sudo mkdir -p ${INSTALL_PACKAGET_PATH}
cd ${INSTALL_PACKAGET_PATH}

# install python3
sudo wget ${PYTHON3_URL}
sudo tar zxvf ${PYTHON3_PACKET}
cd ${PYTHON3_NAME}
sudo ./configure
sudo make
sudo make install
cd ../

python3_test=`sudo ${PYTHON3_BIN_PATH} -V`
if [ -z "$python3_test" ]; then
    echo "!!!!!! python3 install failed !!!!!!"
    exit 0
fi

# install ffmpeg
sudo cpanm Digest::MD5
sudo wget ${FFMPEG_URL}
sudo tar zxvf ${FFMPEG_PACKET}
cd ${FFMPEG_NAME}
sudo sh install_ffmpeg.sh
cd ../

ffmpeg_test=`sudo ${FFMPEG_BIN_PATH} -version`
if [ -z "$ffmpeg_test" ]; then
    echo "!!!!!! ffmpeg install failed !!!!!!"
    exit 0
fi

# install redis
sudo yum -y install redis
sudo sed -i 's/^daemonize no$/daemonize yes/g' /etc/redis.conf
sudo sed -i 's/^# requirepass foobared$/requirepass foobared/g' /etc/redis.conf
sudo systemctl enable redis

redis_server_test=`sudo ${REDIS_BIN_PATH} -v`
if [ -z "$redis_server_test" ]; then
    echo "!!!!!! redis install failed !!!!!!"
    exit 0
fi

# install x100speed_transcode python3 require package
sudo /usr/local/bin/pip3 install ${REQUIRE_PYTHON3_MODULE} -i ${PIP3_SOURCE}
python_module_test=$?
if [ "$python_module_test" !=  "0" ]; then
    echo "!!!!!! pip3 install module failed !!!!!!"
fi

# install x100speed_transcode
cd ${APP_PATH}

sudo wget ${X100SPEED_TRANSCODE_URL}
sudo tar zxvf ${X100SPEED_TRANSCODE_PACKET}
cd ${X100SPEED_TRANSCODE_NAME}

sudo \cp ./ci/x100speed_transcode.service /usr/lib/systemd/system
sudo systemctl enable x100speed_transcode

sudo reboot
