#!/usr/bin/env python
import os, configparser

def load_config(configfile):
    configfile = 'conf/transcoder.conf'
    if not os.path.exists(configfile):
        print("no config file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(configfile)
    return config
