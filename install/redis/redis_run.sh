#!/bin/sh

/usr/local/bin/redis-server /etc/redis.conf;
redis_server_check=$?;
if [ $redis_server_check -eq 0 ]; then
    echo "redis server start succ";
else
    echo "!!!!!!!! redis server start failed !!!!!!!!";
    exit 1;
fi

sleep 30;

init_video_id=`/usr/local/bin/redis-cli -a foobared SET video_id_max 100000`
if [ "$init_video_id" != 'OK' ]; then
    echo "!!!!!!!! init video max id failed !!!!!!!!";
    exit 1;
else
    echo "init video max id succ";
fi
