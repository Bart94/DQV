import hashlib
import pickle
import secrets
from datetime import date, timedelta

DMR = 30


class User:
    __slots__ = ['sk0', 'sk', 't0', 't', 'tpast', 'r', 'r_a', 'r_pa', 'h_a', 'pa', 'city', 'address']

    def __init__(self):
        self.sk0 = secrets.token_hex(32)
        self.t0 = date.today()

    def set_sk(self, t=date.today()):
        self.t = date.today()
        self._eval_sk(t)

    def _eval_sk(self, t):
        self.sk = self.sk0

        diff = (t - self.t0).days
        for i in range(diff):
            self.sk = hashlib.sha256(self.sk.encode('utf-8')).hexdigest()

    def calcolo_pa(self, city, address):
        self.r = secrets.token_hex(10)
        self.r_a = secrets.token_hex(10)
        self.r_pa = secrets.token_hex(10)
        self.city = city
        self.address = address

        self.h_a = hashlib.sha256((self.r_a + self.address).encode('utf-8')).hexdigest()
        self.pa = hashlib.sha256((self.r_pa + self.city + self.h_a + str(DMR)).encode('utf-8')).hexdigest()

    def hash_generator(self, cat, city, address):
        self.calcolo_pa(city, address)

        h = []
        data = ()

        # Caso 1
        if cat:
            self.set_sk()
            h = [hashlib.sha256((self.sk + str(self.t) + self.r + self.pa).encode('utf-8')).hexdigest()]
            data = (h, self.t)
        # Caso 2
        else:
            self.tpast = date.today() - timedelta(days=14)
            self.set_sk(self.tpast)

            h = [hashlib.sha256((self.sk0 + str(self.tpast) + self.r + 'test').encode('utf-8')).hexdigest(),
                 hashlib.sha256((self.sk0 + str(self.tpast) + self.r + self.pa + 'test').encode('utf-8')).hexdigest()]

            data = (h, self.tpast)

        with open('user', 'wb') as f:
            pickle.dump(data, f)

        return h


if __name__ == "__main__":
    user = User()
    user.hash_generator(True, 'Napoli', 'Via Roma 8')

    with open('user', 'rb') as f:
        data = pickle.load(f)
        print(data)
