import socket
import threading
import time
from pynput import keyboard

# Connection vars
SERVER_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096
CHECK_INTERVAL = 2  # Heartbeat interval

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pressed = False
connection_active = False

def connect_to_server():
    """Connect to the server with retries in case of error."""
    global connection_active
    while not connection_active:
        try:
            s.connect(SERVER_ADDRESS)
            connection_active = True
            print("Connected to server.")
        except socket.error as e:
            print(f"Connection error: {e}. Retrying in 5 seconds.")
            time.sleep(5)

def hb_send():
    """Send a heartbeat signal periodically to keep the connection active."""
    global connection_active
    while connection_active:
        try:
            if s.fileno() != -1:  # Check if socket is still open
                s.sendall("heartbeat".encode())
            else:
                connection_active = False
        except socket.error as e:
            print(f"Error sending heartbeat: {e}, reconnecting.")
            connection_active = False
            reconnect()
        time.sleep(CHECK_INTERVAL)

def send_command(command, value):
    """Send commands only if connection is active."""
    if connection_active:
        try:
            message = f"{command}|{value}"
            if s.fileno() != -1:  # Check if socket is still open
                s.sendall(message.encode())
            else:
                print("Connection interrupted.")
                reconnect()
        except socket.error:
            print("Error sending command, reconnecting.")
            reconnect()

def reconnect():
    """Try to reconnect to the server."""
    global connection_active
    connection_active = False
    s.close()
    connect_to_server()

def on_press(key):
    global pressed
    if hasattr(key, 'char') and key.char and not pressed:
        if key.char == "w":
            print("Press W")
            send_command("forward", "1")  # Example value 1 seconds
            pressed = True
        elif key.char == "a":
            print("Press A")
            send_command("left", "1")
            pressed = True
        elif key.char == "d":
            print("Press D")
            send_command("right", "1")
            pressed = True
        elif key.char == "s":
            print("Press S")
            send_command("backward", "1")
            pressed = True
        elif key.char == "q":
            print("Closing.")
            return False  # Stop listener to close the program

def on_release(key):
    global pressed
    if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
        print(f"Release {key.char}")
        pressed = False

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    # Initial connection
    connect_to_server()

    # Start heartbeat thread
    threading.Thread(target=hb_send, daemon=True).start()

    # Start keyboard listener
    start_listener()
