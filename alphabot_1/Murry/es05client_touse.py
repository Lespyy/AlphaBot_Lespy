import socket
import threading
import time
from pynput import keyboard

"""
    Autore: Danilo Rinaldi Mattia Mauro

    Data: 22/10/2024

    Server TCP monoconnessione
"""


# Connection vars
SERVER_ADD = ("192.168.1.138", 9090)
BUFFER_SIZE = 4096

# Global vars
sock_list = []
run = True
connected = False
pressed = False
active_keys = set()  # Keep track of currently pressed keys

def reconnect_socket(sock_type):
    """
    Function to attempt reconnection of the socket in case of disconnection.
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

def send_movement(command, action):
    """
    Sends movement commands only if the connection is active.
    """
    global move_sock
    message = f"{command}|{action}"
    move_sock.sendall(message.encode())

def hb_send():
    """
    Heartbeat function to check connection.
    If connection is lost, attempts to reconnect.
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
    Thread to send commands to the server.
    """
    global connected, run, move_sock

    while run:
        if not connected:
            move_sock = reconnect_socket("Comandi")
            connected = True

        start_listener()

def on_press(key):
    """
    Detects key presses and sends the corresponding command to the server.
    """
    global active_keys, run

    if hasattr(key, 'char') and key.char:
        if key.char in ['w', 'a', 's', 'd'] and key.char not in active_keys:
            active_keys.add(key.char)
            print(f"Press {key.char}")
            send_movement(key.char, "start")

def on_release(key):
    """
    Detects key releases to stop the corresponding movement.
    """
    global active_keys

    if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
        if key.char in active_keys:
            active_keys.remove(key.char)
            print(f"Release {key.char}")
            send_movement(key.char, "stop")

def start_listener():
    """
    Starts listening to keyboard inputs.
    """
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    # Thread for handling heartbeat and commands
    hb_thr = threading.Thread(target=hb_send)
    cmd_thr = threading.Thread(target=cmd_send)
    hb_thr.start()
    cmd_thr.start()
