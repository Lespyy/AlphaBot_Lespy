import threading
import socket
#import alpha_bot as ab

MY_ADD = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096
is_connected = False
run = True

#Alphabot
##Lespy = ab.AlphaBot()

"""
    Autore: Danilo Rinaldi Mattia Mauro
    Data: 10/10/2024
    Server TCP monoconnessione
"""

#global vars

sock_list = []

def cmd_send(command, value):

    move_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    move_sock.bind(MY_ADD)
    move_sock.listen()
    connection, client_address = move_sock.accept()
    sock_list.append(move_sock)
    global is_connected, run
    while run:
        while connection:

            start_listener()

    print("command closed")

def hb_send():
    
    global connection, run
    hb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hb_sock.bind(MY_ADD)
    hb_sock.listen()
    connection, client_address = hb_sock.accept()
    print(f"Il client {client_address} si è connesso con l'HEARTBEAT")

    sock_list.append(hb_sock)
    is_connected = True
    check = 5
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






if __name__ == "__main__":

    hb_thr= threading.Thread(target = hb_send)
    cmd_thr= threading.Thread(target = cmd_send)
    hb_thr.start()
    cmd_thr.start()