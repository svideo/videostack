from flask import Flask
from flask import make_response
import redis

app = Flask(__name__)

@app.route("/")
def hello():
    return "x100speed_transcode"

@app.route("/getvideomaxid")
def getvideomaxid():
    r      = redis.StrictRedis(host='localhost', port=6379, db=0, password='foobared')
    max_id = r.incr("video_id_max")
    resp   = make_response( str(max_id) )
    
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    
    return resp

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
