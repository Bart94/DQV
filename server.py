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
    pa = d['pa']
    t_test = t + timedelta(days=14)

    res = 'Registrazione fallita.'

    if time is None:  # Caso 1
        h_t_check = data.hash_caso_1()

        if h_t_check in at.keys():
            ac, t_check = at[h_t_check]
            if t_check == t:
                message = str(t_check) + h_t_check + 'check'
                sk_t_check = sk

                if verify(message, ac):
                    if sk_t_check not in risk.keys():
                        risk[sk_t_check] = (t_check, pa)
                        res = (sk_t_check, t_check, 3)
                        print('È stato aggiunto un nuovo utente a rischio che ha richiesto il monitoraggio.')
                        del (at[h_t_check])

    elif time > t_test:  # Caso 2.B
        h_m_t_past = data.hash_caso_2_b()

        if h_m_t_past in at.keys():
            ac, t_result = at[h_m_t_past]

            if t_result == time:
                t_past = t
                message = str(t_result) + str(t_past) + h_m_t_past + 'negtest'

                if verify(message, ac):
                    diff = (t_result - t_past).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    sk_t_result = sk

                    if sk_t_result not in risk.keys():
                        risk[sk_t_result] = (t_result, pa)
                        res = (sk_t_result, t_result, 3)
                        print('È stato aggiunto un nuovo utente negativo al tampone che ha richiesto il monitoraggio.')
                        del (at[h_m_t_past])

    elif pa is None:  # Caso 2.A.1
        h_t_past = data.hash_caso_2_a_1()

        if h_t_past in at.keys():
            ac, t_contag = at[h_t_past]

            if t_contag == time:
                t_past = t
                message = str(t_contag) + str(t_past) + h_t_past + 'postest'
                if verify(message, ac):
                    diff = (t_contag - t_past).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    sk_t_contag = sk

                    if sk_t_contag not in infected.keys():
                        infected[sk_t_contag] = (t_contag, None)
                        res = 'Positività Comunicata.'
                        print('È stato aggiunto un nuovo utente infetto che non ha richiesto il monitoraggio.')
                        del (at[h_t_past])
    else:  # Caso 2.A.2
        h_m_t_past = data.hash_caso_2_a_2()

        if h_m_t_past in at.keys():
            ac, t_contag = at[h_m_t_past]

            if t_contag == time:
                t_past = t
                message = str(t_contag) + str(t_past) + h_m_t_past + 'postest'
                if verify(message, ac):
                    diff = (t_contag - t_past).days
                    for i in range(diff):
                        sk = hashlib.sha256(sk.encode('utf-8')).hexdigest()

                    sk_t_contag = sk

                    if sk_t_contag not in infected.keys():
                        infected[sk_t_contag] = (t_contag, pa)
                        res = (sk_t_contag, t_contag, 1)
                        print('È stato aggiunto un nuovo utente infetto che ha richiesto il monitoraggio.')
                        del (at[h_m_t_past])

    return res


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('DQV_certs/serv_cert.pem', 'DQV_certs/serv_sk.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((host, port))
    sock.listen(5)
    print('Server in ascolto...\n')
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            data = conn.recv(1024)
            if not data:
                break
            retrieve_data = pickle.loads(data)

            if isinstance(retrieve_data, DataLab):
                print("Ricevute tuple di attivazione dal laboratorio: " + str(retrieve_data))
                lab_handler(retrieve_data)
            else:
                res = user_handler(retrieve_data)
                print("Invio all'utente: " + str(res))
                print('--------------------')
                conn.send(pickle.dumps(res))
