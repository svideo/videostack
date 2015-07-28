from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import socketserver
import os
import sys
import re


class X100Logger:

    def __init__(self):
        self.logger = logging.getLogger()
        formatter = logging.Formatter(
            "\n\n  Error:\n  line: %(lineno)d of %(pathname)s\n  %(message)s\n")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)


class X100Request:

    def __init__(self):
        self.route_type = ""
        self.remote_ip = ""
        self.query_string = ""
        self.body = ""
        self.headers = dict()
        self.args = dict()
        self.args_in_url = dict()

    def get_remote_ip(self):
        return self.remote_ip

    def get_query_string(self):
        return self.query_string

    def get_body(self):
        return self.body

    def get_header(self, key):
        if key in self.headers:
            return self.headers[key]
        else:
            return ""

    def get_arg(self, key):
        if key in self.args:
            return self.args[key]
        elif key in self.args_in_url:
            return self.args_in_url[key]
        else:
            return ""

    def get_arg_in_url(self, key):
        if key in self.args_in_url:
            return self.args_in_url[key]
        else:
            return ""


class X100Response:

    def __init__(self):
        self.headers = dict()
        self.body = ""

    def set_body(self, body):
        if type(body) is bytes:
            self.body = body
        else:
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
    routers_get_regex = dict()
    routers_post = dict()
    routers_upload = dict()
    routers_static = dict()
    static_file_ext = frozenset(
        ['ico', 'css', 'js', 'html', 'png', 'bmp', 'jpg'])
    upload_buf_size = 4096
    logger = X100Logger()

    def make_x100response(self, response):
        if isinstance(response, X100Response):
            if not "Content-type" in response.headers:
                response.headers["Content-type"] = "text/html"
        else:
            body = response
            response = X100Response()
            response.set_header("Content-type", "text/html")
            response.set_body(body)
        return response

    def send_x100response(self, response):
        self.send_response(200)
        for k in response.headers.keys():
            self.send_header(k, response.headers[k])
        self.end_headers()
        self.wfile.write(response.body)

    def _handle_body(self, line):
        try:
            self.upload_cls.upload_process(self._content_key, line)
        except:
            self.__class__.logger.logger.warning(
                "upload_process() def exec error. ", exc_info=True, stack_info=False)
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
            req = X100Request()
            req.remote_ip = self.address_string()
            if len(file_path) > 1:
                req.query_string = file_path[1]
            req.args = X100HTTPServerHelper.parse_query_string(
                req.query_string)

            self._boundary = content_type.split('boundary=', maxsplit=1)[1]
            self.buf = b''
            self._status_content = "HEAD"  # HEAD, BODY
            self._content_key = ""
            new_line = ''
            buf = ''

            # init function
            try:
                self.upload_cls = self.__class__.routers_upload[
                    self.file_path_without_query_string]()
                self.upload_cls.upload_start(req)
            except:
                self.__class__.logger.logger.warning(
                    "upload_start() def exec error. ", exc_info=True, stack_info=False)
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
                response = self.upload_cls.upload_finish(req)
                response = self.make_x100response(response)
            except:
                self.__class__.logger.logger.warning(
                    "upload_finish() def exec error. ", exc_info=True, stack_info=False)
                self.send_error(500)
            else:
                self.send_x100response(response)

        elif post_type == "application/x-www-form-urlencoded":
            if self.file_path_without_query_string in self.__class__.routers_post:
                req = X100Request()
                req.remote_ip = self.address_string()
                req.body = self.rfile.read(content_length).decode()
                if len(file_path) > 1:
                    req.query_string = file_path[1]
                req.args = X100HTTPServerHelper.parse_query_string(
                    req.body)

                try:
                    response = self.__class__.routers_post[
                        self.file_path_without_query_string](req)
                    response = self.make_x100response(response)
                except:
                    self.__class__.logger.logger.warning(
                        "post_handler() def exec error. ", exc_info=True, stack_info=False)
                    self.send_error(500)
                else:
                    self.send_x100response(response)
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
            req = X100Request()
            req.remote_ip = self.address_string()
            if len(file_path) > 1:
                req.query_string = file_path[1]
            req.args = X100HTTPServerHelper.parse_query_string(
                req.query_string)

            try:
                response = self.__class__.routers_get[
                    self.file_path_without_query_string](req)
                response = self.make_x100response(response)
            except:
                self.__class__.logger.logger.warning(
                    "get_handler() def exec error. ", exc_info=True, stack_info=False)
                self.send_error(500)
            else:
                self.send_x100response(response)
        else:
            for patten in self.__class__.routers_get_regex:
                result = patten.fullmatch(self.file_path_without_query_string)
                if result:
                    req = X100Request()
                    req.remote_ip = self.address_string()
                    if len(file_path) > 1:
                        req.query_string = file_path[1]
                    req.args = X100HTTPServerHelper.parse_query_string(
                        req.query_string)
                    req.args_in_url = result.groupdict()
                    try:
                        response = self.__class__.routers_get_regex[
                            patten](req)
                        response = self.make_x100response(response)
                    except:
                        self.__class__.logger.logger.warning(
                            "regex_get_handler() def exec error. ", exc_info=True, stack_info=False)
                        self.send_error(500)
                    else:
                        self.send_x100response(response)
                    return

            if file_ext in self.__class__.static_file_ext and os.path.exists(file_basename):
                self.send_response(200)
                self.send_header(
                    "Content-type", X100HTTPServerHelper.get_mime(self.file_path_without_query_string))
                self.end_headers()
                f = open(file_basename, "rb", buffering=0)
                os.sendfile(self.wfile.fileno(), f.fileno(), 0, 0)
                f.close()
            else:
                for patten in self.__class__.routers_static:
                    result = patten.fullmatch(
                        self.file_path_without_query_string)
                    if result:
                        static_file_path = self.__class__.routers_static[
                            patten] + result.group(1).split('?')[0]
                        if os.path.exists(static_file_path):
                            self.send_response(200)
                            self.send_header(
                                "Content-type", X100HTTPServerHelper.get_mime(self.file_path_without_query_string))
                            self.end_headers()
                            f = open(static_file_path, "rb", buffering=0)
                            os.sendfile(self.wfile.fileno(), f.fileno(), 0, 0)
                            f.close()
                            return
                self.send_error(404)


class ForkingHTTPServer(socketserver.ForkingMixIn, HTTPServer):

    def finish_request(self, request, client_address):
        HTTPServer.finish_request(self, request, client_address)


class X100HTTP:

    def __init__(self):
        self.logger = X100Logger()
        special_chars = re.escape('+!@#$%^*()')
        self.special_chars = 'a-zA-Z0-9' + special_chars

    def set_upload_buf_size(self, buf_size):
        X100HTTPServer.upload_buf_size = buf_size

    def get(self, url, fn):
        if url[:1] != '/':
            self.logger.logger.warning("Route rule MUST begin with '/'.")
            return
        if '<' in url and '>' in url:
            url_regex = url
            pattern = url.replace('<', '(?P<')
            pattern = pattern.replace(
                '>', '>[' + self.special_chars + ']+)')
            prog = re.compile(pattern)
            X100HTTPServer.routers_get_regex[prog] = fn
        else:
            X100HTTPServer.routers_get[url] = fn

    def post(self, url, fn):
        if url[:1] != '/':
            self.logger.logger.warning("Route rule MUST begin with '/'.")
            return
        X100HTTPServer.routers_post[url] = fn

    def upload(self, url, upload_cls):
        if url[:1] != '/':
            self.logger.logger.warning("Route rule MUST begin with '/'.")
            return
        X100HTTPServer.routers_upload[url] = upload_cls

    def static(self, url_prefix, absolute_path):
        if url_prefix[:1] != '/':
            self.logger.logger.warning("Route rule MUST begin with '/'.")
            return
        pattern = url_prefix + "([" + self.special_chars + "\_\.]+)"
        prog = re.compile(pattern)
        X100HTTPServer.routers_static[prog] = absolute_path

    def run(self, ip, port):
        s = ForkingHTTPServer((ip, port), X100HTTPServer)
        s.serve_forever()
