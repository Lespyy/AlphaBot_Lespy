#failed, check ex 5

import socket
import threading
import time
from pynput import keyboard

# Connection vars
SERVER_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096
CHECK_INTERVAL = 1.5  # Intervallo per l'heartbeat

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pressed = False
connection_active = False



def connect_to_server():
    """Connette al server, con tentativi di riconnessione in caso di errore."""
    global connection_active
    while not connection_active:
        try:
            s.connect(SERVER_ADDRESS)
            connection_active = True
            print("Connessione stabilita con il server.")
            is_hb = threading.Thread(target = hb_send)  # Verifica lo stato della connessione
        except socket.error as e:
            print(f"Errore di connessione: {e}. Riprovo tra 5 secondi.")
            time.sleep(5)

def hb_send():
    """Invia un segnale periodico al server per mantenere la connessione attiva."""
    global connection_active
    while connection_active:
        try:
            if s.fileno() != -1:  # Verifica che il socket sia ancora aperto
                s.sendall("heartbeat".encode())
            else:
                connection_active = False
        except socket.error:
            print("Errore durante l'invio del heartbeat, riconnessione necessaria.")
            connection_active = False
        global is_hb
        is_hb.settimeout(CHECK_INTERVAL)

def send_command(command, value):
    """Invia i comandi solo se la connessione è attiva."""
    if connection_active:
        try:
            message = f"{command}|{value}"
            if s.fileno() != -1:  # Verifica che il socket sia ancora aperto
                s.sendall(message.encode())
            else:
                print("Connessione interrotta.")
                reconnect()
        except socket.error:
            print("Errore durante l'invio del comando, riconnessione necessaria.")
            reconnect()

def reconnect():
    """Tenta di ristabilire la connessione."""
    global connection_active
    connection_active = False
    s.close()
    connect_to_server()

def on_press(key):
    global pressed
    if hasattr(key, 'char') and key.char and not pressed:
        if key.char == "w":
            print("press w")
            send_command("forward", "1")  # Esempio valore 1 secondi
            pressed = True
        elif key.char == "a":
            print("press a")
            send_command("left", "1")
            pressed = True
        elif key.char == "d":
            print("press d")
            send_command("right", "1")
            pressed = True
        elif key.char == "s":
            print("press s")
            send_command("backward", "1")
            pressed = True
        elif key.char == "q":
            print("chiudi")

def on_release(key):
    global pressed
    if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
        print(f"release {key.char}")
        pressed = False

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    # Connessione iniziale
    connect_to_server()
    
    # Avvia l'heartbeat in un thread separato
    
    # Avvia il listener della tastiera
    start_listener()
