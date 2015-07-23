import subprocess, re


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


if __name__ == "__main__":
    process_ffmpeg = process_find('ffmpeg')
    print(process_ffmpeg)
    print("ffmpeg count: %d" % len(process_ffmpeg))



