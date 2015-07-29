from transcoder import Transcoder
from x100http import  X100HTTP, X100Response


app = X100HTTP()
app.upload("/upload", Transcoder)
app.run("0.0.0.0", 8080)
