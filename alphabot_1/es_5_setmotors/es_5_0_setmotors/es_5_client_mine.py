import socket 
import threading
from pynput import keyboard

"""
    Autore: Danilo Rinaldi Mattia Mauro
    Data: 10/10/2024
    Server TCP monoconnessione
"""

#global vars
sock_list = []
run = True

#connection vars

SERVER_ADD = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

connection = False

"""Sockets and threadings"""

#Movements

    #move_sock
    #cmd_thr



def cmd_send():

    move_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_list.append(move_sock)
    global connection, run
    while run:
        while connection:

            start_listener()

    print("command closed")


def send_movement(command, value):
    """Invia i comandi solo se la connessione è attiva."""
    global move_sock
    message = f"{command}|{value}"
    move_sock.sendall(message.encode())




def hb_send():
    
    global connection, run
    hb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hb_sock.connect(SERVER_ADD)
    connection = True
    sock_list.append(hb_sock)
    check = 1.5
    while run:
        while connection:

            try:

                hb_sock.sendall(("Can you hear me?").encode())

            except socket.timeout:
                
                print("disconnessione")
                connection = False
                #reconnect

            except Exception as e:

                print(f"exception throw: {e}")
    print("hb_closed")

    
        
            
def on_press(key):
    global pressed, run
    if hasattr(key, 'char') and key.char and not pressed:

        if key.char == "w":
            print("press w")
            send_movement("forward", "1")  # Esempio valore 1 secondi
            pressed = True

        elif key.char == "a":
            print("press a")
            send_movement("left", "1")
            pressed = True

        elif key.char == "d":
            print("press d")
            send_movement("right", "1")
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
    global pressed
    if hasattr(key, 'char') and key.char in ['w', 'a', 's', 'd']:
        print(f"release {key.char}")
        pressed = False
    
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



if __name__ == "__main__":

    hb_thr= threading.Thread(target = hb_send)
    cmd_thr= threading.Thread(target = cmd_send)
    hb_thr.start()
    cmd_thr.start()
    