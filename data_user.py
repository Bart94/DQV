from Crypto.Hash import SHA256


class DataUser:
    __slots__ = ['sk', 't', 'r', 'pa', 'time']

    def __init__(self, sk, t, r, pa=None, time=None):
        self.sk = sk
        self.t = t
        self.r = r
        self.pa = pa
        self.time = time

    def get_info(self):
        return {'sk': self.sk, 't': self.t, 'r': self.r, 'pa': self.pa, 'time': self.time}

    def get_sk(self):
        return self.sk

    def get_t(self):
        return self.t

    def hash_caso_1(self):
        return SHA256.new((self.sk + str(self.t) + self.r + self.pa).encode('utf-8')).hexdigest()

    def hash_caso_2_a_1(self):
        return SHA256.new((self.sk + str(self.t) + self.r + 'test').encode('utf-8')).hexdigest()

    def hash_caso_2_b(self):
        return SHA256.new((self.sk + str(self.t) + self.r + self.pa + 'test').encode('utf-8')).hexdigest()

    def hash_caso_2_a_2(self):
        return self.hash_caso_2_b()
