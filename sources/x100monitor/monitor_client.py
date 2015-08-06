import argparse, socket, sys, os, configparser, urllib, time
from x100daemon import Daemon
from x100monitor import x100Monitor
from optparse import OptionParser


def load_config(configfile):
    if not os.path.exists(configfile):
        print("no config file")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(configfile)
    return config

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

def http_callback(url, info):
    request_url = url + '?' + info
    request = urllib.request.Request(request_url)
    with urllib.request.urlopen(request) as f:
        return json.loads(f.read().decode('utf-8'))

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

    interval = int(config['monitor']['interval'])
    want_process = config['monitor']['want_process'].rstrip('"')

    if args.daemonize:
        pidfile = '/var/run/monitor_client.pid'
        d = Daemon(pidfile)
        d.daemonize()

    local_ip = get_local_ip()

    m = x100Monitor()

    while True:

        time.sleep(interval)

        process_info = m.process(want_process)
        process_count = len(process_info)

        request_info = 'ip=' + local_ip + '&process_count=' + str(process_count)
        try:
            res = http_callback('http://10.221.193.64/interface/update_staff_monitor', request_info)
        except:
            print("call update staff monitor interface error")
            continue

        if res['status'] == 'failed':
            print('error: %s' % res['message'])
        else:
            print('success')





if __name__ == "__main__":
    main()
