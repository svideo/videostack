|

NAME
====

    x100http, web framework support customing file upload processing


|

SYNOPSIS
========

.. code-block::


    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(request):
        remote_ip = request.get_remote_ip()
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)


|

DESCRIPTION
===========

    x100http is a lite webframework designed for processing HTTP file upload.


|

CLASS X100HTTP
==============

X100HTTP()
----------
    return a instance of x100http which wrapped below functions.

run(listern_ip, listen_port)
----------------------------
    run a forking server on address ``listern_ip``:``listern_port``

get(url, handler_function)
--------------------------
    set a route acl of HTTP "GET" method.

    ``handler_function`` will be called when ``url`` be visited.

    ``handler_function`` must return a string as the HTTP response body to the visitor.

    struct ``request`` (will explain below) will be passed to the handlder function when it is called.

post(url, handler_function)
---------------------------
    set a route acl of HTTP "POST" method with header "Content-Type: application/x-www-form-urlencoded".

    ``handler_function`` will be called when HTTP client submit a form with the action ``url``.

    ``handler_function`` must return a string as the HTTP response body to the visitor.

    struct ``request`` (will explain below) will be passed to the handlder function when it is called.

static(url_prefix, file_path)
-----------------------------
    set a route acl for static file

    Static file request with ``url_prefix`` will be routing to the file in ``file_path``.

upload(url, upload_handler_class)
---------------------------------
    set a route acl of HTTP "POST" method with header "Content-Type: multipart/form-data".

    A new instance of class ``upload_handler_class`` will be created when file upload start.

    struct "request" (will explain below) will be passed to ``upload_handler_class.upload_start()``.

    ``upload_handler_class.upload_process()`` will be called every time when the buffer is full when file uploading.

    two args will be passed to ``upload_handler_class.upload_process()``.

    first arg is the name of the input in the form, second arg is the content of the input in the form.

    the binary content of the upload file will be passed by the second arg.

    struct "request" (will explain below) will NOT be passed to ``upload_handler_class.upload_finish()``.

    ``upload_handler_class.upload_finish()`` will be called when file upload finished, this function must return a string as the HTTP response body to the visitor.

    struct "request" (will explain below) will be passed to ``upload_handler_class.upload_finish()``.

set_upload_buf_size(buf_size)
-----------------------------
    set the buffer size of the stream reader while file uploading.

    the unit of ``buf_size`` is byte, default value is 4096 byte.

    ``upload_handler_class.upload_process()`` will be called to process the buffer every time when the buffer is full.


|

ROUTING
=======

    x100http route accept a url and a function/class/path.

    There are three four of routes - get, post, static and upload.

.. code-block::

    app.get("/get_imple", get_simple)
    app.post("/post_simple", post_simple)
    app.upload("/upload_simple", UploadClass)
    app.static("/static/test/", "/tmp/sta/")

routing for HTTP GET can be more flexible like this:

.. code-block::

    app.get("/one_dir/<arg_first>_<arg_second>.py?abc=def", regex_get)


|

CLASS X100REQUEST
=================

    A instance of class ``X100Request`` will be passed into every handler function.

get_remote_ip()
---------------
    Return the IP address of the visitor.

get_body()
----------
    Return the body section of the HTTP request.

    Will be empty when the HTTP method is "GET" or "POST - multipart/form-data".

get_query_string()
------------------
    Return the query string of the page was accessed, if any.

get_arg(arg_name)
-----------------

    args parsed from ``query_string`` when the request is sent by "GET" or "POST - multipart/form-data".

    args parsed from ``body`` when the request is sent by "POST - application/x-www-form-urlencoded".

get_header(header_name)
-----------------------
    Return the header`s value of the ``header_name``, if any.


|

CLASS X100RESPONSE
==================

set_body(content)
-----------------

    Set the response data to visitor.

    Type 'str' and type 'bytes' are both accepted.

set_header(name, value)
-----------------------

    Set the HTTP header.


|

HTTP ERROR 500
==============

    visitor will get HTTP error "500" when the handler function of the url he visit raise an error or code something wrong.


|

SUPPORTED PYTHON VERSIONS
=========================

    x100http only supports python 3.4 or newer.


|

EXAMPLES
========

get visitor ip
--------------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(request):
        remote_ip = request.get_remote_ip()
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)

post method route
-----------------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()

    def index(request):
        response = "<html><body>" \
            + "<form name="abc" action="/form" method="post">" \
            + "<input type="text" name="abc" />" \
            + "<input type="submit" name="submit" />" \
            + "</form>" \
            + "</body></html>"
        return response

    def post_handler(request):
        remote_ip = request.get_remote_ip()
        abc = request.get_arg('abc')
        response = "hello, " + remote_ip + " you typed: " + abc
        return response

    app.get("/", index)
    app.post("/form", post_handler)
    app.run("0.0.0.0", 8080)

process file upload
-------------------

.. code-block::

    from x100http import X100HTTP, X100Response

    class UploadHandler:

        def upload_start(self, request):
            self.content = "start"

        def upload_process(self, key, line):
            self.content += line.decode()

        def upload_finish(self, request):
            return "upload succ, content = " + self.content

    app = X100HTTP()
    app.upload("/upload", UploadHandler)
    app.run("0.0.0.0", 8080)

set http header
---------------

.. code-block::

    from x100http import X100HTTP, X100Response

    def get_custom_header(request):
        remote_ip = request.get_remote_ip()
        response = X100Response()
        response.set_header("X-My-Header", "My-Value")
        response.set_body("<html><body>hello, " + remote_ip + "</body></html>")
        return response

    app = X100HTTP()
    app.upload("/", get_custom_header)
    app.run("0.0.0.0", 8080)

more flexible routing
---------------------

.. code-block::

    from x100http import X100HTTP

    def regex_get(request):
        first = request.get_arg("arg_first")
        second = request.get_arg("arg_second")
        abc = request.get_arg("abc")
        return "hello, " + first + second + abc

    app = X100HTTP()
    app.get("/one_dir/<arg_first>_<arg_second>.py?abc=def", regex_get)
    app.run("0.0.0.0", 8080)
