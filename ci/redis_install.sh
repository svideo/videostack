#!/bin/sh

mkdir -p /data/install
cd /data/install

# install redis server
yum -y install tcl tcl-devel
wget http://download.redis.io/releases/redis-3.0.2.tar.gz
tar zxvf redis-3.0.2.tar.gz
cd redis-3.0.2
make
make test
make install
sed -i 's/^daemonize no$/daemonize yes/g' ./redis.conf
sed -i 's/^# requirepass foobared$/requirepass foobared/g' ./redis.conf
\cp -rf redis.conf /etc/

redis_server_cmd=`/usr/local/bin/redis-server -v > /dev/null 2>&1`;
redis_server_check=$?;
if [ $redis_server_check -eq 0 ]; then
    echo "redis server install succ";
else
    echo "!!!!!!!! redis server install failed !!!!!!!!";
fi
