import socket
import threading
import time
from pynput import keyboard

SERVER_ADD = ("192.168.1.138", 9094)
BUFFER_SIZE = 4096

# Global variables
run = True
connected = False
active_keys = set()

def reconnect_socket():
    """
    Attempts to reconnect to the server.
    """
    global connected
    while not connected and run:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(SERVER_ADD)
            print("[CLIENT] Reconnected successfully.")
            connected = True
            return sock
        except Exception as e:
            print(f"[CLIENT] Reconnection failed, retrying in 5 seconds: {e}")
            time.sleep(5)

def hb_send(sock):
    """
    Sends heartbeat signals to the server.
    """
    global connected, run
    while run:
        try:
            if not connected:
                sock = reconnect_socket()
            sock.sendall("Can you hear me?".encode())
            time.sleep(1.5)
        except Exception as e:
            print(f"[CLIENT] Heartbeat error: {e}")
            connected = False

def send_movement(sock, command, action):
    """
    Sends movement commands to the server.
    """
    try:
        message = f"{command}|{action}"
        sock.sendall(message.encode())
    except Exception as e:
        print(f"[CLIENT] Command error: {e}")
        connected = False

def keyboard_listener(sock):
    """
    Listens for keyboard inputs and sends commands to the server.
    """
    def on_press(key):
        if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
            if key.char not in active_keys:
                active_keys.add(key.char)
                send_movement(sock, key.char, "start")

    def on_release(key):
        if hasattr(key, 'char') and key.char in active_keys:
            active_keys.remove(key.char)
            send_movement(sock, key.char, "stop")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    client_sock = reconnect_socket()
    threading.Thread(target=hb_send, args=(client_sock,)).start()
    keyboard_listener(client_sock)
