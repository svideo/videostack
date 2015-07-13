from flask import Flask, request
from flask import make_response
import redis
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome X100speed_transcode Admin System'

@app.route('/x100speedtranscode/videostaff/add')
@app.route('/x100speedtranscode/videostaff/updata')
def video_staff_add():
    ip = request.args.get('ip')
    if(not ip):
        return "{'status':'failed', 'message':'ip is null'}"
    
    load = request.args.get('load')
    if(not load):
        return "{'status':'failed', 'message':'load is null'}"

    r = redis_connect()
    r.hset("video_staff_hash", ip, load)
    
    return "{'status':'success', 'message':''}"

@app.route('/x100speedtranscode/videostaff/delete')
def video_staff_delete():
    ip = request.args.get('ip')
    if(not ip):
        return "{'status':'failed', 'message':'ip is null'}"
    
    r = redis_connect()
    r.hset("video_staff_hash", ip)

    return "{'status':'success', 'message':''}"

def redis_connect():
    host='127.0.0.1'
    port=6379
    db=0
    password='foobared'

    r = redis.StrictRedis(host = host, port = port, password = password, db = db)
    return r


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
