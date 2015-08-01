#!/usr/bin/evn python
import x100redis

def redis_conn(self):
    r = redis.StrictRedis(host=self.config['redis']['ip'], port=self.config['redis']['port'], db=0)
    return r

def insert_redis(self, score, member):
    r = self.redis_conn()
    zz_key = self.segment_list_name
    print(self.segment_list_name)
    print(member)
    r.zadd(zz_key, score, member)
    r.expire(zz_key, self.config['segment']['expire'])
    info("insert redis ok")
    return 1

def remove_redis(self, zz_key, member):
    r = self.redis_conn()
    zz_key = self.segment_list_name
    r.zrem(zz_key, member)
    info("delete redis ok")
    return 1

