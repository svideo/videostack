from x100http import X100HTTP, X100Response

app = X100HTTP()

def get_simple(req):
    remote_ip = req['remote_ip']
    response = "<html><body>hello, " + remote_ip + "</body></html>"
    return response

def get_via_class(req):
    remote_ip = req['remote_ip']
    response = X100Response()
    response.set_body("<html><body>hello, " + remote_ip + "</body></html>")
    return response

def get_via_class_directly(req):
    remote_ip = req['remote_ip']
    response = X100Response()
    response.body = ("<html><body>hello, " + remote_ip + "</body></html>").encode()
    return response

def get_custom_header(req):
    remote_ip = req['remote_ip']
    response = X100Response()
    response.set_header("X-My-Header", "My-Value")
    response.set_body("<html><body>hello, " + remote_ip + "</body></html>")
    return response

def get_custom_header_directly(req):
    remote_ip = req['remote_ip']
    response = X100Response()
    response.headers["X-My-Header"] = "My-Value"
    response.body = ("<html><body>hello, " + remote_ip + "</body></html>").encode()
    return response

app.get("/", get_simple)
app.get("/get_via_class", get_via_class)
app.get("/get_via_class_directly", get_via_class_directly)
app.get("/get_custom_header", get_custom_header)
app.get("/get_custom_header_directly", get_custom_header_directly)

app.run("0.0.0.0", 8080)
