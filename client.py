import os
import socket as Socket


def connect_to(conn_type, server_addr, server_port):
    message = "Hello, word!"

    if conn_type == "TCP":
        s = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
        s.connect((server_addr, server_port))
        s.send(message.encode('UTF-8'))
        print('Message: "' + message + '" sent to server TCP')
        data = s.recv(1024)
        print('Received from the server TCP:', str(data.decode('utf-8')))
        s.close()
    elif conn_type == "UDP":
        s = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
        s.sendto(message.encode('utf8'), (server_addr, server_port))
        print('Message: "' + message + '" sent to server UDP')
        data, serverAddr = s.recvfrom(1024)
        print('Received from the server UDP:', str(data.decode('utf8')))
    else:
        print('Parametri inseriti non validi!')


if __name__ == "__main__":
    cls = lambda: os.system('cls')

    while True:
        conn_type = input("Inserici il tipo di connessione: ").upper();
        print(conn_type)
        server_addr = input("Inserici indirizzo server: ")
        print(server_addr)
        server_port = input("Inserisci il numero di porta del server: ")
        print(server_port)
        connect_to(conn_type, server_addr, int(server_port))
        clear_on = input("Vuoi pulire la console?\n1]yes\n2]no")
        if (clear_on == "1") or (clear_on.upper() == "YES"):
            cls()
