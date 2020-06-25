import pickle
import socket
import ssl
from datetime import timedelta, date

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from data_lab import DataLab

HOST = "localhost"
PORT = 443


class Laboratorio:
    __slots__ = ['h_utenti', 'sk', 'pk']

    def __init__(self):
        self.h_utenti = {}
        self.sk = ECC.import_key(open('DQV_certs/lab_sk.pem').read())

    def add_user(self, h, t):
        index = len(self.h_utenti)
        self.h_utenti[index] = (h, t)
        return index

    def act_tuple_generator(self, index, test=None, time=date.today()):
        (h, t) = self.h_utenti[index]

        t_test = t + timedelta(days=14)

        print(t, t_test, time)

        act_tuple = []

        if test == 'negtest':
            if time > t_test:
                with open('time', 'wb') as f:
                    pickle.dump(time, f)

                msg = str(time) + str(t) + h[0] + test
                h_msg = SHA256.new(msg.encode('utf-8'))
                signer = DSS.new(self.sk, 'fips-186-3')
                ac = signer.sign(h_msg)
                act_tuple.append((ac, h[0], time))
        # Caso 2.A
        elif test == 'postest':
            if t <= time <= t_test:
                with open('time', 'wb') as f:
                    pickle.dump(time, f)

                for elem in h:
                    msg = str(time) + str(t) + elem + test
                    print('msg', str(time), str(t), elem, test)
                    h_msg = SHA256.new(msg.encode('utf-8'))
                    signer = DSS.new(self.sk, 'fips-186-3')
                    ac = signer.sign(h_msg)
                    print('elem', elem)
                    act_tuple.append((ac, elem, time))
        else:
            msg = str(t) + h[0] + 'check'
            h_msg = SHA256.new(msg.encode('utf-8'))
            signer = DSS.new(self.sk, 'fips-186-3')
            ac = signer.sign(h_msg)
            act_tuple.append((ac, h[0], t))

        return act_tuple

    def send_act_tuple(self, act_tuple):
        message = pickle.dumps(act_tuple)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as s_sock:
                s_sock.connect((HOST, PORT))
                s_sock.send(message)


# if __name__ == "__main__":
#     lab = Laboratorio()
#
#     with open('user', 'rb') as f:
#         h, t = pickle.load(f)
#
#     lab.add_user(h, t)
#     ac = DataLab(lab.act_tuple_generator(0, 'postest', date.today()))
#     lab.send_act_tuple(ac)
