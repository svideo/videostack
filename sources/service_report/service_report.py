#!/usr/bin/env python3
import time
import argparse
import sys
import socket
import configparser
import os
from x100daemon import Daemon


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def load_config(configfile):
    if not os.path.exists(configfile):
        print("no config file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(configfile)
    return config

def main():
    useage = '''

    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemonize", help="make daemonize", action="store_true")
    parser.add_argument("-f", "--config", help="assign config file path")

    args = parser.parse_args()

    if not args.config:
        print("please assign config file path")
        sys.exit(1)

    configfile = args.config
    config = load_config(configfile)

    interval = int(config['service_report']['interval'])
    local_ip = get_local_ip()


    if args.daemonize:
        pidfile = '/var/run/service_report.pid'
        d = Daemon(pidfile)
        d.daemonize()

    while True:
        request_info = 'ip=' + local_ip

        try:
            res = http_callback(config['service_report']['callback'], request_info)
        except:
            print("call update staff monitor interface error")
            time.sleep(interval)
            continue

        if res['status'] == 'failed':
            print('error: %s' % res['message'])
        else:
            print('success')
            sys.exit(0)

        time.sleep(interval)


if __name__ == "__main__":
    main()
