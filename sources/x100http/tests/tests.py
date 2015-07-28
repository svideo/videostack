import unittest
import time
import urllib.request
from multiprocessing import Process
from x100http import X100HTTP, X100Response
import requests


class UploadHandler:

    def upload_start(self, req):
        self.content = "start"

    def upload_process(self, key, line):
        self.content += line.decode()

    def upload_finish(self, req):
        return "upload succ, content = " + self.content


def get_simple(req):
    remote_ip = req.get_remote_ip()
    response = "<html><body>hello, " + remote_ip + "</body></html>"
    return response


def get_via_class(req):
    remote_ip = req.get_remote_ip()
    response = X100Response()
    response.set_body("<html><body>hello, " + remote_ip + "</body></html>")
    return response


def get_via_class_directly(req):
    remote_ip = req.get_remote_ip()
    response = X100Response()
    response.body = (
        "<html><body>hello, " + remote_ip + "</body></html>").encode()
    return response


def get_args(req):
    myval = req.get_arg("myget_key")
    return "hello" + myval


def get_query_string(req):
    return "hello" + req.get_query_string()


def get_custom_header(req):
    remote_ip = req.get_remote_ip()
    response = X100Response()
    response.set_header("X-My-Header", "My-Value")
    response.set_body("<html><body>hello, " + remote_ip + "</body></html>")
    return response


def get_custom_header_directly(req):
    remote_ip = req.get_remote_ip()
    response = X100Response()
    response.headers["X-My-Header"] = "My-Value"
    response.body = (
        "<html><body>hello, " + remote_ip + "</body></html>").encode()
    return response


def post_simple(req):
    return "hello, world!" + req.get_body()


def post_urlencode(req):
    return "hello, world!" + req.get_arg('mykey')

def regex_get(req):
    arg_first = req.get_arg("arg_first")
    arg_second = req.get_arg("arg_second")
    return "regex_get: " + arg_first + ", " + arg_second

def regex_get_in_url(req):
    arg_first = req.get_arg_in_url("arg_first")
    arg_second = req.get_arg_in_url("arg_second")
    return "regex_get: " + arg_first + ", " + arg_second

def regex_get_more_arg(req):
    arg_first = req.get_arg("arg_first")
    arg_second = req.get_arg("abc")
    return "regex_get: " + arg_first + ", " + arg_second

class TestSimple(unittest.TestCase):

    @classmethod
    def setUpClass(ConnectionHolder):
        app = X100HTTP()
        app.get("/", get_simple)
        app.get("/get_via_class", get_via_class)
        app.get("/get_via_class_directly", get_via_class_directly)
        app.get("/get_args", get_args)
        app.get("/get_query_string", get_query_string)
        app.get("/get_custom_header", get_custom_header)
        app.get("/get_custom_header_directly", get_custom_header_directly)
        app.post("/post_simple", post_simple)
        app.post("/post_urlencode", post_urlencode)
        app.upload("/upload_simple", UploadHandler)
        app.get("/one_dir/<arg_first>_<arg_second>.py", regex_get)
        app.get("/<arg_first>_<arg_second>.py", regex_get_in_url)
        app.get("/one_dir/<arg_first>.py", regex_get_more_arg)
        app.static("/static/test/", "tests/sta/")
        ConnectionHolder.p = Process(target=app.run, args=('127.0.0.1', 8080))
        ConnectionHolder.p.start()

    @classmethod
    def tearDownClass(ConnectionHolder):
        ConnectionHolder.p.terminate()

    def test_static(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/tests/test.html', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.info().get('Content-Type'), 'text/html')
        self.assertEqual(f.read().decode(), "this is test.html\n")

    def test_static_simple(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/static/test/static_test.html', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.info().get('Content-Type'), 'text/html')
        self.assertEqual(f.read().decode(), "this is test for static html\n")

    def test_get_root(self):
        req = urllib.request.Request(url='http://127.0.0.1:8080', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_get_root_slash(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_get_via_class(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_via_class', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_get_via_class_directly(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_via_class_directly', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_get_args(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_args?myget_key=myget_value', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.read().decode(), "hellomyget_value")

    def test_get_query_string(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_query_string?myget_key=myget_value', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.read().decode(), "hellomyget_key=myget_value")

    def test_get_custom_header(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_custom_header', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.info().get('X-My-Header'), 'My-Value')
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_get_via_class_directly(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/get_custom_header_directly', method='GET')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.info().get('X-My-Header'), 'My-Value')
        self.assertEqual(
            f.read().decode(), "<html><body>hello, 127.0.0.1</body></html>")

    def test_post_simple(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/post_simple', data=b'data', method='POST')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.read().decode(), "hello, world!data")

    def test_post_urlencode(self):
        req = urllib.request.Request(
            url='http://127.0.0.1:8080/post_urlencode', data=b'mykey=myvalue', method='POST')
        f = urllib.request.urlopen(req)
        self.assertEqual(f.status, 200)
        self.assertEqual(f.read().decode(), "hello, world!myvalue")

    def test_upload_simple(self):
        f = open('tests/test.html', 'rb')
        r = requests.post(
            'http://127.0.0.1:8080/upload_simple', files={'file': f})
        f.close()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.text, "upload succ, content = startthis is test.html\n\r\n")

    def test_regex_get(self):
        resp = requests.get('http://127.0.0.1:8080/one_dir/hello_x100http.py')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "regex_get: hello, x100http")

    def test_regex_get_404(self):
        resp = requests.get('http://127.0.0.1:8080/one_dir/hello_x100http.pl')
        self.assertEqual(resp.status_code, 404)

    def test_regex_get_in_url(self):
        resp = requests.get('http://127.0.0.1:8080/hello_x100http.py')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "regex_get: hello, x100http")

    def test_regex_get_more_arg(self):
        resp = requests.get('http://127.0.0.1:8080/one_dir/hello.py?abc=def')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "regex_get: hello, def")


if __name__ == '__main__':
    unittest.main()
