import socket
import threading
import time
from pynput import keyboard

# Connection vars
SERVER_ADD = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

# Global vars
sock_list = []
run = True
connected = False
pressed = False

def reconnect_socket(sock_type):
    """
    Funzione per tentare di riconnettere il socket in caso di disconnessione.
    """
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(SERVER_ADD)
            sock_list.append(sock)
            print(f"{sock_type} riconnesso con successo.")
            return sock
        except Exception as e:
            print(f"Riconnessione fallita ({sock_type}), ritento in 5 secondi: {e}")
            time.sleep(5)


def send_movement(command, value):
    """
    Invia i comandi solo se la connessione è attiva.
    """
    global move_sock
    message = f"{command}|{value}"
    move_sock.sendall(message.encode())


def hb_send():
    """
    Funzione per inviare l'heartbeat periodico.
    Se la connessione si perde, tenta di riconnettersi.
    """
    global connected, run, move_sock
    while run:
        if not connected:
            move_sock = reconnect_socket("Heartbeat")
            connected = True

        try:
            move_sock.sendall("Can you hear me?".encode())
            time.sleep(1.5)

        except Exception as e:
            print(f"Heartbeat error: {e}")
            connected = False


def cmd_send():
    """
    Thread per inviare comandi al server.
    """
    global connected, run, move_sock

    while run:
        if not connected:
            move_sock = reconnect_socket("Comandi")
            connected = True

        start_listener()


def on_press(key):
    """
    Rileva la pressione dei tasti e invia i comandi al server.
    """
    global pressed, run
    if hasattr(key, 'char') and key.char and not pressed:
        if key.char == "w":
            print("press w")
            send_movement("forward", "1")
            pressed = True
        elif key.char == "a":
            print("press a")
            send_movement("left", "0.5")
            pressed = True
        elif key.char == "d":
            print("press d")
            send_movement("right", "0.5")
            pressed = True
        elif key.char == "s":
            print("press s")
            send_movement("backward", "1")
            pressed = True
        elif key.char == "q":
            for sock in sock_list:
                sock.close()
            run = False
            print("chiudo tutto")


def on_release(key):
    """
    Rileva il rilascio dei tasti per fermare i comandi.
    """
    global pressed
    if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
        print(f"release {key.char}")
        pressed = False


def start_listener():
    """
    Inizia ad ascoltare i tasti della tastiera.
    """
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    # Thread per gestire heartbeat e comandi
    hb_thr = threading.Thread(target=hb_send)
    cmd_thr = threading.Thread(target=cmd_send)
    hb_thr.start()
    cmd_thr.start()
