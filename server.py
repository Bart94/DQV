import hashlib
import pickle
import socket
import ssl
from datetime import timedelta

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from data_lab import DataLab

risk = {}
infected = {}
at = {}
host = 'localhost'
port = 443


def verify(message, ac):
    key = ECC.import_key(open('DQV_certs/lab_pk.pem').read())
    h = SHA256.new(message.encode('utf-8'))
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, ac)
        return True
    except ValueError:
        return False


def lab_handler(data):
    act_tuple = data.get_act_tuple()
    act_m_tuple = data.get_act_m_tuple()

    if act_tuple is not None:
        at[act_tuple['h']] = (act_tuple['ac'], act_tuple['t'])
    at[act_m_tuple['h']] = (act_m_tuple['ac'], act_m_tuple['t'])


def user_handler(data):
    d = data.get_info()

    sk = d['sk']
    time = d['time']
    t = d['t']
    print('caso2b', time, t)
    t_test = t + timedelta(days=14)
    pa = d['pa']

    res = 'Ops! Sono contrariato.'

    if time is None:  # Caso 1
        h_msg = data.hash_caso_1()

        if h_msg in at.keys():
            ac, t_check = at[h_msg]
            if t_check == t:
                message = str(t) + h_msg + 'check'
                if verify(message, ac):
                    if sk not in risk.keys():
                        risk[sk] = (t, pa)
                        res = (sk, t, 3)
                        del (at[h_msg])

    elif time > t_test:  # Caso 2.B
        h_msg = data.hash_caso_2_b()

        if h_msg in at.keys():
            ac, t_result = at[h_msg]

            if t_result == time:
                message = str(time) + str(t) + h_msg + 'negtest'
                if verify(message, ac):
                    diff = (time - t).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    if sk not in risk.keys():
                        risk[sk] = (time, pa)
                        res = (sk, time, 3)
                        del (at[h_msg])

    elif pa is None:  # Caso 2.A.1
        print('Caso2a1')
        h_msg = data.hash_caso_2_a_1()

        if h_msg in at.keys():
            ac, t_contag = at[h_msg]

            if t_contag == time:
                message = str(time) + str(t) + h_msg + 'postest'
                if verify(message, ac):
                    diff = (time - t).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    if sk not in infected.keys():
                        infected[sk] = (time, None)
                        res = 'Ok. Guglielmo.'
                        del (at[h_msg])
    else:  # Caso 2.A.2
        print('Caso2a2')
        h_msg = data.hash_caso_2_a_2()
        print('HELLO', h_msg)
        if h_msg in at.keys():
            print('Ivan')
            ac, t_contag = at[h_msg]
            if t_contag == time:
                print('ac,t', ac, t_contag)
                message = str(time) + str(t) + h_msg + 'postest'
                print(str(time), str(t), h_msg, 'postest')
                if verify(message, ac):
                    diff = (time - t).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    if sk not in infected.keys():
                        infected[sk] = (time, pa)
                        res = (sk, time, 1)
                        del (at[h_msg])

    return res


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('DQV_certs/serv_cert.pem', 'DQV_certs/serv_sk.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((host, port))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            data = conn.recv(1024)
            if not data:
                break
            retrieve_data = pickle.loads(data)

            if isinstance(retrieve_data, DataLab):
                lab_handler(retrieve_data)
                print('DataLab', at)
            else:
                res = user_handler(retrieve_data)
                print('user', res)
                conn.send(pickle.dumps(res))
                print('at', at)
                print('risk', risk)
                print('infected', infected)
