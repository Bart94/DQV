import hashlib
import pickle
import secrets
import socket
import ssl
from datetime import date, timedelta

from data_user import DataUser

HOST = "localhost"
PORT = 443
DMR = 30


class Utente:
    __slots__ = ['sk0', 'sk', 't0', 't', 'tpast', 'r', 'r_a', 'r_pa', 'h_a', 'pa', 'city', 'address', 'sk_t_m', 't_m',
                 'v_max']

    def __init__(self):
        self.sk0 = secrets.token_hex(32)
        self.t0 = date.today() - timedelta(days=20)
        self.t = date.today() - timedelta(days=1)

    def set_sk(self, t=date.today() - timedelta(days=1)):
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

    def hash_generator(self, tampone, city, address):
        self.calcolo_pa(city, address)

        # Caso 1
        if not tampone:
            self.set_sk()
            h = [hashlib.sha256((self.sk + str(self.t) + self.r + self.pa).encode('utf-8')).hexdigest()]
            data = (h, self.t)
        # Caso 2
        else:
            self.tpast = self.t - timedelta(days=14)
            self.set_sk(self.tpast)

            h = [hashlib.sha256((self.sk + str(self.tpast) + self.r + self.pa + 'test').encode('utf-8')).hexdigest(),
                 hashlib.sha256((self.sk + str(self.tpast) + self.r + 'test').encode('utf-8')).hexdigest()]

            data = (h, self.tpast)

        with open('user', 'wb') as f:
            pickle.dump(data, f)

        return h

    def sign_in_procedure(self, tampone, positivo=True, monitoraggio=True):
        if not tampone:
            if monitoraggio:  # Caso 1
                data = DataUser(self.sk, self.t, self.r, self.pa)
        else:
            with open('time', 'rb') as f:
                time = pickle.load(f)

            if positivo and not monitoraggio:  # Caso 2.A.1
                data = DataUser(self.sk, self.tpast, self.r, pa=None, time=time)
            elif monitoraggio:  # Caso 2.A.2 - Caso 2.B
                data = DataUser(self.sk, self.tpast, self.r, self.pa, time)

        return data

    def send_user_info(self, data):
        message = pickle.dumps(data)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as s_sock:
                s_sock.connect((HOST, PORT))
                s_sock.send(message)
                byte_stream = s_sock.recv(1024)

                retrieve_data = pickle.loads(byte_stream)
                if isinstance(retrieve_data, tuple):
                    self.sk_t_m, self.t_m, self.v_max = retrieve_data
                    print('Parametri Monitoraggio')
                    print('SK: ' + self.sk_t_m + ' - T: ' + str(self.t_m) + ' - VMax: ' + str(self.v_max) + '\n')
                else:
                    print(retrieve_data + '\n')

        return retrieve_data
