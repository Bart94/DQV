import pickle
import socket
import ssl
from datetime import date, timedelta

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

HOST = "localhost"
PORT = 8081


class Laboratorio:
    __slots__ = ['h_utenti', 'sk', 'pk']

    def __init__(self):
        self.h_utenti = {}
        self.sk = ECC.import_key(open('DQV_certs/lab_sk.pem').read())

    def add_user(self, h, t):
        index = len(self.h_utenti)
        self.h_utenti[index] = (h, t)

    def ac_generator(self, index, test=None, time=None):
        (h, t) = self.h_utenti[index]

        t_test = t + timedelta(days=14)

        ac = []

        if test == 'negtest':
            if time >= t_test:
                with open('time', 'wb') as f:
                    pickle.dump(time, f)

                msg = str(time) + str(t) + h[0] + test
                h_msg = SHA256.new(msg.encode('utf-8'))
                signer = DSS.new(self.sk, 'fips-186-3')
                signature = signer.sign(h_msg)
                ac.append((signature, h[0], time))
        # Caso 2.A
        elif test == 'postest':
            if t <= time <= t_test:
                with open('time', 'wb') as f:
                    pickle.dump(time, f)

                for elem in h:
                    msg = str(time) + str(t) + elem + test
                    h_msg = SHA256.new(msg.encode('utf-8'))
                    signer = DSS.new(self.sk, 'fips-186-3')
                    signature = signer.sign(h_msg)
                    ac.append((signature, elem, time))
        else:
            msg = str(t) + h[0] + 'check'
            h_msg = SHA256.new(msg.encode('utf-8'))
            signer = DSS.new(self.sk, 'fips-186-3')
            signature = signer.sign(h_msg)
            ac.append((signature, h[0], t))

        return ac

    def send_ac(self, ac):
        message = pickle.dumps(ac)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_sock = context.wrap_socket(sock, server_hostname=HOST)
        s_sock.connect((HOST, PORT))
        s_sock.send(message)
        s_sock.close()


if __name__ == "__main__":
    lab = Laboratorio()

    with open('user', 'rb') as f:
        h, t = pickle.load(f)

    lab.add_user(h, t)
    print(lab.ac_generator(0, date.today()))
