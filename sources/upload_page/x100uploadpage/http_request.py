#!/usr/bin/env python3
from x100http import X100HTTP
from transcoder import Transcoder

app = X100HTTP()

transcode = Transcoder('conf/transcoder.conf')

def upload_init(req):
    transcode.init_popen_handler()
    return


def upload_ing(key, body):
    if key == b'video_id':
        video_id = body.decode().rstrip()
        print(key)
        print(video_id)
    else:
        pass
        #print(body)
        #self.video_id = video_id
        #self.init_popen_handler()
        #res = update_video_status(transcode.config['url']['update_video_status'], self.video_id, 'proceed', str(self.bitrate))
        #if res['status'] == 'failed':
        #    logging.error("video_id: %s callbackApi: update_video_status error: %s", self.video_id, res['message'])
        #    return
        #elif(name == b'upload'):
        #    transcode.run_cmd_async(body)

def upload_finish(req):
    print("abcdefgh_done")
    return "your file uploaded."

app.upload("/abc", upload_init, upload_ing, upload_finish)

app.run("0.0.0.0", 80)
