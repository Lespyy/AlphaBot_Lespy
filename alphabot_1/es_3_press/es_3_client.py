from pynput import keyboard

import socket

SERVER_ADDRESS = ("192.168.1.138", 9090)
BUFFER_SIZE = 4096

pressed = False

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(SERVER_ADDRESS)

def on_press(key):
    global pressed
    if key.char == "w":
        if not pressed:
            print("press w")
            message = "forward|1"
            #s.sendall(message.encode())
            #message = s.recv(BUFFER_SIZE)
        pressed = True

    if key.char == "a":
        if not pressed:
            print("press a")
            message = "left|1"
            #s.sendall(message.encode())
            #message = s.recv(BUFFER_SIZE)
        pressed = True

    if key.char == "d":
        if not pressed:
            print("press d")
            message = "right|1"
            #s.sendall(message.encode())
            #message = s.recv(BUFFER_SIZE)
        pressed = True

    if key.char == "s":
        if not pressed:
            print("press s")
            message = "backward|1"
            #s.sendall(message.encode())
            #message = s.recv(BUFFER_SIZE)
        pressed = True


def on_release(key):
    global pressed
    if key.char == "w":
        if pressed:
            print("release w")
        pressed = False
    elif key.char == "a":
        if pressed:
            print("release a")
        pressed = False
    elif key.char == "d":
        if pressed:
            print("release d")
        pressed = False
    elif key.char == "s":
        if pressed:
            print("release s")
        pressed = False

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("start")
        listener.join()

start_listener()
