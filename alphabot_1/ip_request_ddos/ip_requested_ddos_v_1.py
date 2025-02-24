import socket
import time

BUFFER_SIZE = 4096

def send_command(server_ip, server_port, command, value):
    try:
        # Crea una socket TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))

        # Prepara e invia il messaggio
        message = f"{command}|{value}"
        s.send(message.encode())

        # Ricevi la risposta del server
        response = s.recv(BUFFER_SIZE).decode()
        print(f"Risposta dal server: {response}")

        # Chiudi la connessione
        s.close()

    except Exception as e:
        print(f"Errore durante la connessione al server: {e}")

if __name__ == '__main__':
    # Richiedi l'indirizzo IP e la porta da tastiera
    server_ip = input("Inserisci l'indirizzo IP del server: ")
    server_port = int(input("Inserisci la porta del server: "))

    # Esempio di invio di un numero elevato di richieste
    for i in range(100):  # Sostituisci 100 con il numero desiderato di richieste
        send_command(server_ip, server_port, "forward", 2)  # Invia il comando 'avanti' con valore 2 secondi
        time.sleep(0.001)  # Attendi 1ms tra una richiesta e l'altra
