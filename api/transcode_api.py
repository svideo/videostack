from flask import Flask
import redis

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getvideomaxid")
def getvideomaxid():
    r      = redis.StrictRedis(host='localhost', port=6379, db=0, password='foobared')
    max_id = r.incr("video_id_max")
    return str(max_id)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
