import hashlib
import secrets
from datetime import date

DMR = 30


class User:
    __slots__ = ['sk0', 'sk', 't0', 't', 'r', 'r_a', 'r_pa', 'h_a', 'pa', 'city', 'address']

    def __init__(self):
        self.sk0 = secrets.token_hex(32)
        self.t0 = date.today()

    def set_sk(self):
        self.t = date.today()
        self.sk = self.sk0

        diff = (self.t - self.t0).days

        for i in range(diff):
            self.sk = hashlib.sha256(self.sk).digest()

    def calcolo_pa(self, city, address):
        self.r = secrets.token_hex(10)
        self.r_a = secrets.token_hex(10)
        self.r_pa = secrets.token_hex(10)
        self.city = city
        self.address = address

        self.h_a = hash(self.r_a + self.address)
        self.pa = hash(self.r_pa + self.city + self.h_a + DMR)