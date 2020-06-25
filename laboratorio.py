import pickle
import socket
import ssl
from datetime import timedelta, date

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

HOST = "localhost"
PORT = 443


class Laboratorio:
    __slots__ = ['db_utenti', 'sk_lab']

    def __init__(self):
        self.db_utenti = {}
        self.sk_lab = ECC.import_key(open('DQV_certs/lab_sk.pem').read())

    def add_user(self, h, t):
        index = len(self.db_utenti)
        self.db_utenti[index] = (h, t)
        return index

    def act_tuple_generator(self, index, test=None, time=date.today()):
        (h, t) = self.db_utenti[index]

        t_test = t + timedelta(days=14)
        act_tuple = []

        if test == 'negtest':  # Caso 2.B
            t_result = time
            t_past = t
            h_m_t_past = h[0]
            if t_result > t_test:
                with open('time', 'wb') as f:
                    pickle.dump(t_result, f)

                msg = str(t_result) + str(t_past) + h_m_t_past + test
                h_msg = SHA256.new(msg.encode('utf-8'))
                signer = DSS.new(self.sk_lab, 'fips-186-3')
                ac = signer.sign(h_msg)
                act_tuple.append((ac, h_m_t_past, t_result))
                print("L'utente ha eseguito il test il giorno {}. "
                      "Il risultato è stato negativo il giorno {}".format(t_test, t_result))

        elif test == 'postest':  # Caso 2.A
            t_contag = time
            t_past = t
            if t_past <= t_contag <= t_test:
                with open('time', 'wb') as f:
                    pickle.dump(t_contag, f)

                for elem in h:
                    msg = str(t_contag) + str(t_past) + elem + test
                    h_msg = SHA256.new(msg.encode('utf-8'))
                    signer = DSS.new(self.sk_lab, 'fips-186-3')
                    ac = signer.sign(h_msg)
                    act_tuple.append((ac, elem, t_contag))
                print("L'utente ha eseguito il test il giorno {}. "
                      "Il risultato è stato positivo e l'utente risulta contagioso dal giorno {}".format(t_test,
                                                                                                         t_contag))

        else:  # Caso 1
            t_check = t
            h_t_check = h[0]
            msg = str(t_check) + h_t_check + 'check'
            h_msg = SHA256.new(msg.encode('utf-8'))
            signer = DSS.new(self.sk_lab, 'fips-186-3')
            ac = signer.sign(h_msg)
            act_tuple.append((ac, h_t_check, t_check))
            print("All'utente viene imposta la quarantena il giorno {}".format(t_check))

        return act_tuple

    def send_act_tuple(self, act_tuple):
        message = pickle.dumps(act_tuple)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as s_sock:
                s_sock.connect((HOST, PORT))
                s_sock.send(message)
