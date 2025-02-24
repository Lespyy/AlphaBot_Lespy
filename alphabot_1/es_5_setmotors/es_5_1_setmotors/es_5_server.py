import socket
import threading

# Connection vars
SERVER_ADD = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096

# Global vars
clients = []
run_server = True

def handle_client(connection, client_address):
    """
    Gestisce la connessione e la ricezione di comandi da un singolo client.
    """
    print(f"[CONNESSIONE] Client connesso: {client_address}")

    try:
        while True:
            message = connection.recv(BUFFER_SIZE).decode()
            if not message:
                break

            # Controlla se il messaggio è l'heartbeat o un comando di movimento
            if message == "Can you hear me?":
                print(f"[HEARTBEAT] Ricevuto heartbeat dal client {client_address}")
            else:
                command, value = message.split("|")
                print(f"[COMANDO] Comando ricevuto dal client {client_address}: {command} per {value} secondi")

    except Exception as e:
        print(f"[ERRORE] Errore nella connessione con {client_address}: {e}")
    finally:
        print(f"[DISCONNESSIONE] Client disconnesso: {client_address}")
        connection.close()

def start_server():
    """
    Avvia il server e accetta nuove connessioni.
    """
    global run_server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADD)
    server_socket.listen()
    print(f"[SERVER] In ascolto su {SERVER_ADD}...")

    while run_server:
        try:
            connection, client_address = server_socket.accept()
            clients.append(connection)

            # Avvia un thread per ogni nuovo client connesso
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()

        except KeyboardInterrupt:
            print("[SERVER] Interruzione ricevuta, sto chiudendo il server.")
            break

    # Chiude tutte le connessioni quando il server viene interrotto
    for client in clients:
        client.close()

    server_socket.close()
    print("[SERVER] Chiusura completata.")


if __name__ == "__main__":
    start_server()
