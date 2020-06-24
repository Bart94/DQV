import os
import socket
import ssl

risk = {}
infected = {}
ac = {}
host = 'localhost'
port = 8080

print(os.urandom(2))

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/path/to/certchain.pem', '/path/to/private.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        ...

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address
sock.bind((host, port))
# Put the socket into listening mode; argument specifies the maximum number of connections allowed
sock.listen()
print('Socket in ascolto')

while True:
    # Establish connection with the new client; c is a new socket object to send and receive data on the connection
    conn, addr = sock.accept()
    data = conn.recv(1024)
    if not data:
        break
    print("Il client TCP chiede: ", str(data.decode('utf8')))
    conn.sendto("Hello from TCP server!".encode('utf8'), addr)
    conn.close()
# Close the socket at the end
sock.close()
