NAME
====

    x100http - WebFramework support customing file upload processing



SYNOPSIS
========

.. code-block::


    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(req):
        remote_ip = req['remote_ip']
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)



DESCRIPTION
===========

    x100http is a webframework helps you customing HTTP file upload processing.



METHODS
=======

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


upload(url, handler_function_init, handler_function_process, handler_function_del)
----------------------------------------------------------------------------------
    set a route acl of HTTP "POST" method with header "Content-Type: multipart/form-data".

    ``handler_function_init`` will be called when file upload start.

    struct "request" (will explain below) will be passed to ``handler_function_init``.

    ``handler_function_process`` will be called every time when the buffer is full when file uploading.

    two args will be passed to ``handler_function_process``.

    first arg is the name of the input in the form, second arg is the content of the input in the form.

    the binary content of the upload file will be passed by the second arg.

    struct "request" (will explain below) will NOT be passed to ``handler_function_process``.

    ``handler_function_del`` will be called when file upload finished, this function must return a string as the HTTP response body to the visitor.

    struct "request" (will explain below) will be passed to ``handler_function_del``.


set_upload_buf_size(buf_size)
-----------------------------
    set the buffer size of the stream reader while file uploading.

    the unit of ``buf_size`` is byte, default value is 4096 byte.

    ``handler_function_process`` will be called to process the buffer every time when the buffer is full.



STRUCT REQUEST
==============

    ``request`` will be passed into the handler function you set, you can use these informations in your app logic.

    ``request`` is a dictionary filled with key-values below.

remote_ip
---------
    The IP address of the visitor.


body
----
    The body part of the HTTP request.

    ``body`` is a empty string when the request is sent by HTTP method "GET" or "POST - multipart/form-data".


query_string
------------
    The query string, if any, via which the page was accessed.


args
----
    A dictionary of variables passed to the handler function via the URL parameters.

    ``args`` parse from ``query_string`` when the request is sent by HTTP method "GET" or "POST - multipart/form-data".

    ``args`` parse from ``body`` when the request is sent by HTTP method "POST - application/x-www-form-urlencoded".



PROCESS FILE UPLOAD
===================

    x100http is designed for custom file processing, it can be used to optimize the video transcoding process.

    ``handler_function_init``, ``handler_function_process``, ``handler_function_del`` will be called when file upload.

    you can simulate a traditional file upload processing like this:

    1. open a file in ``handler_function_init``

    2. when ``handler_function_init`` be called, write content to the file

    3. close file in ``handle_function_del``


handler_function_init(request)
------------------------------
    this function will be called when file upload start with arg ``request``.


handler_function_process(name, content)
---------------------------------------
    this function will be called every time x100http read something throught network.

    the function will be called many times when big file uploading, it need to process a part of the file every time.

    ``name`` is the html input`s name.

    ``content`` is the html input`s value, binary file content some.


handler_function_del(request)
-----------------------------
    this function will be called when file upload finished.

    x100http expect a string from this function ues to construct HTTP response.



HTTP ERROR 500
==============

    visitor will get HTTP error "500" when the handler function of the url he visit raise an error or code something wrong.



SUPPORTED PYTHON VERSIONS
=========================

    x100http only supports python 3.3 or newer.



EXAMPLES
========

process get
-----------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()

    def hello_world(req):
        remote_ip = req['remote_ip']
        response = "<html><body>hello, " + remote_ip + "</body></html>"
        return response

    app.get("/", hello_world)
    app.run("0.0.0.0", 8080)


process post
------------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()

    def index(req):
        response = "<html><body>" \
            + "<form name="abc" action="/form" method="post">" \
            + "<input type="text" name="abc" />" \
            + "<input type="submit" name="submit" />" \
            + "</form>" \
            + "</body></html>"
        return response

    def post_handler(req):
        remote_ip = req['remote_ip']
        abc = req['args']['abc']
        response = "<html><body>hello, " + remote_ip + " you typed: " + abc + "</body></html>"
        return response

    app.get("/", index)
    app.post("/form", post_handler)
    app.run("0.0.0.0", 8080)


process file upload
-------------------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()
    fp = ""

    def index(req):
        response = "<html><body>" \
            + "<form name="abc" action="/upload" method="post">" \
            + "<input type="text" name="abc" />" \
            + "<input type="file" name="file_upload" />" \
            + "<input type="submit" name="submit" />" \
            + "</form>" \
            + "</body></html>"
        return response

    def upload_init(req):
        fp = open("upload_file.bin", mode="ab")
        return

    def upload_ing(key, body):
        if name == b'file_upload':
            fp.write(body)
        elif name == b'abc':
            print(body)         
        return

    def upload_finish(req):
        fp.close()
        return req['remote_ip'] + ", your file uploaded."

    app.get("/", index)
    app.upload("/upload", upload_init, upload_ing, upload_finish)

    app.run("0.0.0.0", 8080)

     
a more complex example
----------------------

.. code-block::

    from x100http import X100HTTP

    app = X100HTTP()

    def get_test(req):
        body = req['body']
        abc = req['args']['abc']
        remote_ip = req['remote_ip']

        response = "<html><body>get test succ <br/>" \
            + "body:[" + body + "]<br/>" \
            + "args:[" + abc + "]<br/>" \
            + "ip:[" + remote_ip + "]" \
            + "</body></html>"
        return response


    def post_test(req):
        body = req['body']
        abc = req['args']['abc']
        remote_ip = req['remote_ip']

        response = "<html><body>post test succ <br/>" \
            + "body:[" + body + "]<br/>" \
            + "args:[" + abc + "]<br/>" \
            + "ip:[" + remote_ip + "]" \
            + "</body></html>"
        return response

    def upload_test_init(req):
        print(req['remote_ip'])
        return

    def upload_test_ing(key, body):
        print(key)
        print("write")
        return

    def upload_test_del(req):
        return req['remote_ip']

    app.set_upload_buf_size(8192)
    app.get("/get", get_test)
    app.post("/post", post_test)
    app.upload("/upload", upload_test_init, upload_test_ing, upload_test_del)

    app.run("0.0.0.0", 8080)
     

