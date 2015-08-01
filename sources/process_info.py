import subprocess, re
import socket
import urllib.request
import json

def process_find(find_cmd):
    stats = subprocess.Popen(['pidstat','-ruht'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    stats_data = stats.splitlines()
    del stats_data[0:2] # Deletes system data

    converted_data = []
    for line in stats_data:
        if re.search(b'command', line, re.IGNORECASE):
            header = line.decode().split()
            del header[0]
        else:
            command = line.decode().split()
            cmd = command[-1]
            if cmd != find_cmd:
                continue
            data_dict = dict(zip(header, command))

            process_memory_mb = float(1000) * float(data_dict["%MEM"].replace(',', '.'))
            memory = "{0:.3}".format(process_memory_mb)
            memory = memory.replace(",", ".")

            cpu = "{0:.2f}".format( float( data_dict["%CPU"].replace(",", ".") ) )
            cpu = cpu.replace(",", ".")

            command = data_dict["Command"]
            if not re.search("_", command, re.IGNORECASE):
                extracted_data = { "cpu:%": cpu,
                                  "memory:mb": memory,
                                  "command:" : command}
                converted_data.append(extracted_data)
    return converted_data

def get_ip():
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

if __name__ == "__main__":
    process_ffmpeg = process_find('ffmpeg')
    process_ffmpeg_count = len(process_ffmpeg)
    local_ip = get_ip()
    request_info = 'ip=' + local_ip + '&process_count=' + str(process_ffmpeg_count)
    res = http_callback('http://10.221.193.64/interface/update_staff_monitor', request_info)
    if res['status'] == 'failed':
        print('error: %s' % res['message'])
    else:
        print('success')
