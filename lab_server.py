import secrets

import OpenSSL
from Crypto.PublicKey import ECC


class Laboratorio:

    __slots__ = ['h_utenti', 'sk', 'pk']

    def __init__(self):
        self.h_utenti = {}
        self.sk_l = secrets.token_hex(32)
        self.pk_l = ECC.generate(curve='P-256')

    def add_user(self, h, t):
        index = len(self.h_utenti)
        self.h_utenti[index] = (h, t)

    def ac_generator(self, index):
        (h, t) = self.h_utenti[index]
        ac = []
        # Caso 1
        # if len(h) == 1:



