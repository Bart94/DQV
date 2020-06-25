----------------- DETECTION of QUARANTINE VIOLATION (DQV) -----------------

1. OBIETTIVO
L'applicativo sviluppato permette di simulare la Fase 2 di registrazione descritta nella documentazione del DQV, consentendo l'aggiunta di utenti appartenenti a tutti i casi descritti.

# CERTIFICATI
Per il corretto funzionamento dell'applicativo è stato necessario realizzare i seguenti certificati:
 - certificato laboratorio (lab_cert.pem): al fine di verificare i dati firmati dal laboratorio sfruttando la chiave privata contenuta nel file "lab_sk.pem";
 - certificato server (serv_cert.pem): al fine di consentire la creazione di una connessione sicura su protocollo TLS 1.3 con il server.

Entrambi questi certificati sono stati attivati grazie ad una RootCA appositamente definita nel certificato "cacert.pem".

# ALGORITMI
La funzione di hash utilizzata per la realizzazione dei commitment è SHA-256.
L'algoritmo di firma utilizzato è ECDSA 'P-256'.

Per ulteriori dettagli fare riferimento alla documentazione.


2. REQUISITI
Sono richieste le seguenti librerie per la corretta esecuzione del codice:
- python 3.7
- pyOpenSSL 19.1.0
- pycryptodome 3.9.7


3. ISTRUZIONI
    1. Avviare il file "server.py";
    2. Avviare il file "main.py" e seguire le istruzioni a video per l'aggiunta degli utenti.