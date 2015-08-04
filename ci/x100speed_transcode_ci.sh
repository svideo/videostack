#!/usr/bin/env bash

install_package_path='/data/install'
x100speed_transcode_path='/data'

sudo mkdir -p ${install_package_path}

# disable firewalld
sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo setenforce 0

# init server
sudo yum -y install epel-release git openssl openssl-devel perl-devel
sudo wget  http://xrl.us/cpanm --no-check-certificate -O /sbin/cpanm
sudo chmod +x  /sbin/cpanm

cd ${install_package_path}
# install python3
sudo wget http://10.221.193.64:8000/Python-3.4.3.tgz
sudo tar zxvf Python-3.4.3.tgz
cd Python-3.4.3
sudo ./configure
sudo make
sudo make install
cd ../

# install ffmpeg
sudo cpanm Digest::MD5
sudo wget http://10.221.193.64:8000/ffmpeg_install_2.7.2.tar.gz
sudo tar zxvf ffmpeg_install_2.7.2.tar.gz
cd ffmpeg_install_2.7.2
sudo sh install_ffmpeg.sh
cd ../

# install redis
sudo yum -y install redis
sudo sed -i 's/^daemonize no$/daemonize yes/g' /etc/redis.conf
sudo sed -i 's/^# requirepass foobared$/requirepass foobared/g' /etc/redis.conf
sudo systemctl enable redis
sudo systemctl start redis

# install x100speed_transcode python3 require package
sudo /usr/local/bin/pip3 install redis x100http x100idgen x100daemon -i http://mirrors.aliyun.com/pypi/simple

# install x100speed_transcode
cd ${x100speed_transcode_path}

sudo wget http://10.221.193.64:8000/x100speed_transcode.tar.gz
sudo tar zxvf x100speed_transcode.tar.gz


# run redis server
sudo redis-server /etc/redis.conf
sleep 3

#test x100speed
cd ./x100speed_transcode/sources
#/usr/local/bin/python3 setup.py test
sudo /usr/local/bin/python3 run.py

sleep 3

curl -L "http://10.221.193.64/interface/add_staff_ip?ip=10.221.193.64"
curl -L "http://10.221.193.64/interface/update_staff_monitor?ip=10.221.193.64&process_count=0"
