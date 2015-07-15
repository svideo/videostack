#!/usr/bin/env python

import os
import sys
import configparser
import redis

def read_conf():
    configfile = 'conf/transcoder.conf'
    if not os.path.exists(configfile):
        print("no config file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(configfile)

    return config

def redis_conn(config):
    r = redis.StrictRedis(host=config['redis']['ip'], port=config['redis']['port'], db=0)
    return r

if __name__ == "__main__":
    config = read_conf()
    r = redis_conn(config)
    #r.set('foo', 'bar')
    #print(r.get('foo'))
    #r.expire('foo', 65536)
    r.zadd('what_list', 0, 'sssss|bbbbb|cccc|5')
    r.expire('what_list', config['segment']['expire'])
