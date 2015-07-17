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
    print("aaaaaaaaaaaaaaaaa")
    return

def upload_test_ing(key, body):
    print(key)
    return

def upload_test_del(req):
    return req['remote_ip']

app.get("/get", get_test)
app.post("/post", post_test)
app.upload("/upload", upload_test_init, upload_test_ing, upload_test_del)

app.run("0.0.0.0", 4321)
