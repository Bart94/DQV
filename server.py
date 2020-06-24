import os
import pickle
import socket
import ssl

risk = {}
infected = {}
ac = {}
host = 'localhost'
port = 443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('DQV_certs/serv_cert.pem', 'DQV_certs/serv_sk.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((host, port))
    print(sock.getsockname())
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            data = conn.recv(1024)
            if not data:
                break
            retrieve_data = pickle.loads(data)
