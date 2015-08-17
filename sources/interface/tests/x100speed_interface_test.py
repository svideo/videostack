import os, unittest, redis, requests, json
from multiprocessing import Process
from x100speed_interface import *

class TestSimple(unittest.TestCase):
    video_id = ""
    staff_ip = ""

    @classmethod
    def setUpClass(ConnectionHolder):
        os.system("/usr/local/bin/redis-server /etc/redis.conf")
        app = X100HTTP()

        app.get("/interface/add_staff_ip",                   add_staff_ip)
        app.get("/interface/update_staff_monitor",           update_staff_monitor)
        app.get("/interface/get_video_id",                   get_video_id)
        app.get("/interface/update_video_status",            update_video_status)
        app.get("/interface/get_video_info",                 get_video_info)
        app.get("/interface/update_video_snap_image_count",  update_video_snap_image_count)
        app.get("/interface/get_video_new_snap_image",       get_video_new_snap_image)
        app.get("/interface/add_video_segment",              add_video_segment)
        app.get("/interface/<play_url>.m3u8",                video_play)
        app.get("/interface/<play_url>_<play_bitrate>.m3u8", video_play_child)

        ConnectionHolder.p = Process(target=app.run, args=('127.0.0.1', 5000))
        ConnectionHolder.p.start()
    
    @classmethod
    def tearDownClass(ConnectionHolder):
        os.system("ps auxf |grep redis-server | grep -v grep | awk '{print $2}' |  xargs kill")
        ConnectionHolder.p.terminate()

    def test_add_staff_ip(self):
        payload = {'ip':'127.0.0.1'}
        request = requests.get('http://127.0.0.1:5000/interface/add_staff_ip', params=payload)
        data    = json.loads(request.text)
        
        self.assertEqual(data['status'], 'success')

    def test_update_staff_monitor(self):
        payload = {'ip':'127.0.0.1', 'process_count':'1'}
        request = requests.get('http://127.0.0.1:5000/interface/update_staff_monitor', params=payload)
        data    = json.loads(request.text)
        
        self.assertEqual(data['status'], 'success')

    def test_get_video_id(self):
        payload = {'ip':'127.0.0.1', 'process_count':'0'}
        request = requests.get('http://127.0.0.1:5000/interface/update_staff_monitor', params=payload)
        data    = json.loads(request.text)

        self.assertEqual(data['status'], 'success')

        request = requests.get('http://127.0.0.1:5000/interface/get_video_id')
        data    = json.loads(request.text)

        self.assertTrue(data['video_id'])
        self.assertTrue(data['ip'])

        TestSimple.video_id = data['video_id']
        TestSimple.staff_ip = data['ip']

    def test_update_video_status(self):
        payload = {'video_id': TestSimple.video_id, 'status':'proceed', 'bitrate':'200'}
        request = requests.get('http://127.0.0.1:5000/interface/update_video_status', params=payload)
        data    = json.loads(request.text)

        self.assertEqual(data['status'], 'success')

    def test_get_video_info(self):
        payload = {'video_id': TestSimple.video_id}
        request = requests.get('http://127.0.0.1:5000/interface/get_video_info', params=payload)
        data    = json.loads(request.text)

        self.assertTrue(data['status'])

    def test_z_update_video_snap_image_count(self):
        payload = {'video_id': TestSimple.video_id, 'snap_image_count':'150'}
        request = requests.get('http://127.0.0.1:5000/interface/update_video_snap_image_count', params=payload)
        data    = json.loads(request.text)

        self.assertEqual(data['status'], 'success')

    def test_z_get_video_new_snap_image(self):
        payload = {'video_id': TestSimple.video_id, 'snap_image_count':'150'}
        request = requests.get('http://127.0.0.1:5000/interface/update_video_snap_image_count', params=payload)
        payload = {'video_id': TestSimple.video_id}
        request = requests.get('http://127.0.0.1:5000/interface/get_video_new_snap_image', params=payload)
        data    = json.loads(request.text)

        self.assertTrue(data['image_url'])

    def test_z_add_video_segment(self):
        payload = {
                    'video_id': TestSimple.video_id,\
                    'bitrate' :'200',\
                    'fragment_id':'1',\
                    'hostname':'http://127.0.0.1',\
                    'storage_path':'/8ee/2fa/f2e/yuGfhL4RmEIW8EStFU_0.ts',\
                    'create_time':'1437808633',\
                    'fps':'15',\
                    'frame_count':'150',\
                    'file_size':'1105064'\
                  }
        request = requests.get('http://127.0.0.1:5000/interface/add_video_segment', params=payload)
        data    = json.loads(request.text)

        self.assertEqual(data['status'], 'success')

    def test_z_video_play(self):
        play_url = 'http://127.0.0.1:5000/interface/' + TestSimple.video_id + '.m3u8'
        request  = requests.get(play_url)
        data     = request.text

        self.assertTrue(data)

    def test_z_video_play_child(self):
        play_url = 'http://127.0.0.1:5000/interface/' + TestSimple.video_id + '_200.m3u8'
        request  = requests.get(play_url)
        data     = request.text

        self.assertTrue(data)    

if __name__ == '__main__':
    unittest.main()

