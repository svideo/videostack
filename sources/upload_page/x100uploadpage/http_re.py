#!/usr/bin/env python3
import os, sys, re, select, subprocess, io, time, shutil, logging
import urllib.request
from x100.x100config import load_config
from x100.x100util import *
from x100.x100request import http_callback, update_video_status
from x100http import X100HTTP, X100Response
#from transcoder import Transcoder
from trans import Transcoder


app = X100HTTP()
app.upload("/upload", Transcoder)
app.run("0.0.0.0", 80)
