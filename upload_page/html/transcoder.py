#!/usr/bin/env python

class Transcoder:
    def handle_body(self, name, body):
        #if self._content_key == b"channel_id":
        #    m = hashlib.md5()
        #    m.update( line ) # line is channel_id
        #    self.filename = m.hexdigest() + '.flv'
        #else:
        #    print("filename" + self.filename)
        #    f = open(self.filename, 'ab')
        #    f.write(line)
        #    f.close()
        print("----------------------")
        print(name + b' '+ body)
        print("----------------------")

