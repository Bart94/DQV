import pickle
from datetime import date

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


class Laboratorio:
    __slots__ = ['h_utenti', 'sk', 'pk']

    def __init__(self):
        self.h_utenti = {}
        self.sk = ECC.import_key(open('DQV_certs/lab_sk.pem').read())

    def add_user(self, h, t):
        index = len(self.h_utenti)
        self.h_utenti[index] = (h, t)

    def ac_generator(self, index, t_contag=None):
        (h, t) = self.h_utenti[index]
        ac = []
        # Caso 1
        if len(h) == 1:
            msg = str(t) + h[0] + 'check'
            h_msg = SHA256.new(msg.encode('utf-8'))
            signer = DSS.new(self.sk, 'fips-186-3')
            signature = signer.sign(h_msg)
            ac.append((signature, h[0], t))
        else:
            for elem in h:
                msg = str(t_contag) + str(t) + elem + 'postest'
                h_msg = SHA256.new(msg.encode('utf-8'))
                signer = DSS.new(self.sk, 'fips-186-3')
                signature = signer.sign(h_msg)
                ac.append((signature, elem, t_contag))

        return ac


if __name__ == "__main__":
    lab = Laboratorio()

    with open('user', 'rb') as f:
        h, t = pickle.load(f)

    lab.add_user(h, t)
    print(lab.ac_generator(0, date.today()))
