import hashlib
import time
import random

class IdGeneratorX100:

    def __init__(self, encryt_key):
        self.encryt_key = encryt_key
        self.byte_dict = dict(zip(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                              ], [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
            36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
        ]))
        self.byte_dict_reserve = dict()
        for k in self.byte_dict.keys():
            self.byte_dict_reserve[self.byte_dict[k]] = k
        self.dict_size = len(self.byte_dict.keys())

    def idGen(self, string):
        string_hash = hashlib.new("md5", string.encode()).hexdigest()[12:20]
        ts = int(time.time())
        rand_number = random.randint(268435456, 4294967295)
        uuid = "{0:x}{1}{2:x}".format(ts, string_hash, rand_number)

        short_uuid = self.hex_to_62base(uuid)

        [valid_byte1, valid_byte2] = self.string_sum(short_uuid)
        result = short_uuid + self.byte_dict_reserve[valid_byte1] + self.byte_dict_reserve[valid_byte2]

        return result

    def idValid(self, id_string):
        [valid_byte1, valid_byte2] = self.string_sum(id_string[:-2])
        if self.byte_dict_reserve[valid_byte1] == id_string[-2] and self.byte_dict_reserve[valid_byte2] == id_string[-1] :
            return True
        else:
            return False

    def hex_to_62base(self, hex_string):
        dec = int(hex_string, 16)
        result = ""
        while True:
          if dec < self.dict_size:
            result = self.byte_dict_reserve[dec] + result;
            return result;
          else:
            remain = dec % self.dict_size
            dec = ( dec - remain ) / self.dict_size
            result = self.byte_dict_reserve[remain] + result;

    def string_sum(self, id_string):
        byte_sum = 0
        for byte in id_string:
            byte_sum = byte_sum + self.byte_dict[byte]
        valid_byte1 = byte_sum % self.dict_size
        valid_byte2 = byte_sum * self.encryt_key % self.dict_size
        return [valid_byte1, valid_byte2]

if __name__ == '__main__':
    g = IdGeneratorX100(266)
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3"
    ip = "111.206.116.190"
    vid = g.idGen(ip+ua)
    print(vid)

    if g.idValid("yt7NaHvuNOqSsc6PdM"):
      print("true")
    else:
      print("false")
