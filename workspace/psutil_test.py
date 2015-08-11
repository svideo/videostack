import psutil

for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name'])
        #if pinfo['name'] == 'ffmpeg':
        #    print(pinfo)
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)
        #pass
