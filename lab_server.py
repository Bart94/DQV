import socket

ht = {}
host = 'localhost'
port = 8081

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
