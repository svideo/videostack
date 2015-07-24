from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import os
import sys

class X100Response:

    def __init__(self):
        self.headers = dict()
        self.body = ""

    def set_body(self, body):
        self.body = body.encode()
        
    def set_header(self, key, value):
        self.headers[key] = value

class X100HTTPServerHelper:

    def get_mime(path):
        if os.path.splitext(path)[1] == '.css':
            return "text/css"
        elif os.path.splitext(path)[1] == '.ico':
            return "image/x-icon"
        elif os.path.splitext(path)[1] == '.html':
            return "text/html"
        return ""

    def get_file_basename(path):
        file_basename = path[1:].split('?')[0]
        if file_basename == "":
            file_basename = "index.html"
        return file_basename

    def get_file_ext(path):
        file_ext = os.path.basename(path).split('.')[-1]
        return file_ext

    def parse_query_string(query_string):
        args = dict()
        for query in query_string.split('&'):
            key_value = query.split('=')
            if len(key_value) == 2:
                args[key_value[0]] = key_value[1]
            else:
                args[key_value[0]] = ''
        return args


class X100HTTPServer(BaseHTTPRequestHandler):
    routers_get = dict()
    routers_post = dict()
    routers_upload = dict()
    static_file_ext = frozenset(
        ['ico', 'css', 'js', 'html', 'png', 'bmp', 'jpg'])
    upload_buf_size = 4096

    def _handle_body(self, line):
        try:
            self.__class__.routers_upload[self.file_path_without_query_string][
                'fn_process'](self._content_key, line)
        except:
            print(sys.exc_info()[0], file=sys.stderr)
            return

    def _handle_a_line(self, line):
        boundary = str.encode(self._boundary)
        if line.find(boundary) != -1:
            self._status_content = "HEAD"
            return

        if line == b"\r\n":
            self._status_content = "BODY"
            return

        if self._status_content == "HEAD":
            [http_header_name, http_header_value] = line.split(b": ")
            if http_header_name == b'Content-Disposition':
                values = http_header_value.split(b"; ")
                for value in values:
                    if value.find(b"=\"") == -1:
                        continue
                    [header_name, header_value] = value.split(b"=\"")
                    if header_name == b'name':
                        [content_key, foo] = header_value.split(b"\"")
                        self._content_key = content_key

        elif self._status_content == "BODY":
            self._handle_body(line)

    def do_POST(self):
        content_length = int(self.headers.get_all('Content-Length')[0])
        content_type = self.headers.get_all('Content-Type')[0]
        post_type = content_type.split(';', maxsplit=1)[0]
        file_path = self.path.split('?')
        self.file_path_without_query_string = file_path[0]

        if post_type == "multipart/form-data":
            req = dict()
            req['remote_ip'] = self.address_string()
            req['body'] = ""
            req['query_string'] = ""
            if len(file_path) > 1:
                req['query_string'] = file_path[1]
            req['args'] = X100HTTPServerHelper.parse_query_string(
                req['query_string'])

            self._boundary = content_type.split('boundary=', maxsplit=1)[1]
            self.buf = b''
            self._status_content = "HEAD"  # HEAD, BODY
            self._content_key = ""
            new_line = ''
            buf = ''

            # init function
            try:
                self.__class__.routers_upload[
                    self.file_path_without_query_string]['fn_init'](req)
            except:
                print(sys.exc_info()[0], file=sys.stderr)
                self.send_error(500)
                return

            # handle body
            while content_length > 0:
                want_byte = self.__class__.upload_buf_size
                if content_length > want_byte:
                    buf = self.rfile.read(want_byte)
                else:
                    buf = self.rfile.read(content_length)
                content_length -= want_byte
                self.buf = self.buf + buf

                while True:
                    line_end = self.buf.find(b'\r\n')
                    if line_end == -1:
                        break
                    else:
                        self._handle_a_line(self.buf[:line_end + 2])
                        self.buf = self.buf[line_end + 2:]

            # output response
            try:
                response = self.__class__.routers_upload[
                    self.file_path_without_query_string]['fn_del'](req).encode()
            except:
                print(sys.exc_info()[0], file=sys.stderr)
                self.send_error(500)
            else:
                self.send_response(200)
                self.send_header(
                    "Content-type", "text/html")
                self.end_headers()
                self.wfile.write(response)

        elif post_type == "application/x-www-form-urlencoded":
            if self.file_path_without_query_string in self.__class__.routers_post:
                req = dict()
                req['remote_ip'] = self.address_string()
                req['body'] = self.rfile.read(content_length).decode()
                req['query_string'] = ""
                if len(file_path) > 1:
                    req['query_string'] = file_path[1]
                req['args'] = X100HTTPServerHelper.parse_query_string(
                    req['body'])

                try:
                    response = self.__class__.routers_post[
                        self.file_path_without_query_string](req).encode()
                except:
                    print(sys.exc_info()[0], file=sys.stderr)
                    self.send_error(500)
                else:
                    self.send_response(200)
                    self.send_header(
                        "Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(response)
            else:
                self.send_error(404)
        else:
            self.send_error(415)

    def do_GET(self):
        file_basename = X100HTTPServerHelper.get_file_basename(self.path)
        file_ext = X100HTTPServerHelper.get_file_ext(file_basename)
        self.file_path_without_query_string = self.path.split('?')[0]
        file_path = self.path.split('?')
        self.file_path_without_query_string = file_path[0]

        if self.file_path_without_query_string in self.__class__.routers_get:
            req = dict()
            req['remote_ip'] = self.address_string()
            req['body'] = ""
            req['query_string'] = ""
            if len(file_path) > 1:
                req['query_string'] = file_path[1]
            req['args'] = X100HTTPServerHelper.parse_query_string(
                req['query_string'])

            try:
                response = self.__class__.routers_get[
                    self.file_path_without_query_string](req)
                if isinstance(response, X100Response):
                    if not "Content-type" in response.headers:
                        response.headers["Content-type"] = "text/html"
                else:
                    body = response.encode()
                    response = X100Response()
                    response.set_header("Content-type", "text/html")
                    response.set_body(body)
            except:
                print(sys.exc_info()[0], file=sys.stderr)
                self.send_error(500)
            else:
                self.send_response(200)
                for k in response.headers.keys():
                    self.send_header(k, response.headers[k])
                self.end_headers()
                self.wfile.write(response.body)

        elif file_ext in self.__class__.static_file_ext:
            if os.path.exists(file_basename):
                self.send_response(200)
                self.send_header(
                    "Content-type", X100HTTPServerHelper.get_mime(self.path))
                self.end_headers()
                f = open(file_basename, "rb", buffering=0)
                self.wfile.write(f.readall())
            else:
                self.send_error(404)
        else:
            self.send_error(404)


class ForkingHTTPServer(socketserver.ForkingMixIn, HTTPServer):

    def finish_request(self, request, client_address):
        HTTPServer.finish_request(self, request, client_address)


class X100HTTP:

    def set_upload_buf_size(self, buf_size):
        X100HTTPServer.upload_buf_size = buf_size

    def get(self, url, fn):
        X100HTTPServer.routers_get[url] = fn

    def post(self, url, fn):
        X100HTTPServer.routers_post[url] = fn

    def upload(self, url, fn_init, fn_process, fn_del):
        X100HTTPServer.routers_upload[url] = dict(
            fn_init=fn_init, fn_process=fn_process, fn_del=fn_del)

    def run(self, ip, port):
        s = ForkingHTTPServer((ip, port), X100HTTPServer)
        s.serve_forever()
