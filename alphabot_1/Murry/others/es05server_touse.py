import socket
import threading
from alpha_bot import AlphaBot

"""
    Autore: Danilo Rinaldi Mattia Mauro

    Data: 23/10/2024

    Server TCP monoconnessione
"""

# Connection vars
SERVER_ADD = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096

# Global vars
clients = []
run_server = True
lock = threading.Lock()

# Initialize AlphaBot
Lespy = AlphaBot()
current_left_speed = 0
current_right_speed = 0

def handle_client(connection, client_address):
    """
    Handles a single client connection and processes commands to control the robot.
    """
    global current_left_speed, current_right_speed

    print(f"[CONNESSIONE] Client connesso: {client_address}")

    try:
        while True:
            message = connection.recv(BUFFER_SIZE).decode()
            if not message:
                break

            # Check if the message is heartbeat or a movement command
            if message == "Can you hear me?":
                print(f"[HEARTBEAT] Ricevuto heartbeat dal client {client_address}")
            else:
                command, action = message.split("|")
                with lock:
                    if action == "start":
                        update_movement(command)
                    elif action == "stop":
                        reset_movement(command)

    except Exception as e:
        print(f"[ERRORE] Errore nella connessione con {client_address}: {e}")
        Lespy.stop()
    finally:
        print(f"[DISCONNESSIONE] Client disconnesso: {client_address}")
        connection.close()
        Lespy.stop()

def update_movement(command):
    """
    Updates the movement of the AlphaBot based on the received command.
    """
    global current_left_speed, current_right_speed

    if command == "w":  # forward
        current_left_speed -= 50
        current_right_speed += 50
    elif command == "s":  # backward
        current_left_speed += 50
        current_right_speed -= 50
    elif command == "a":  # left
        current_right_speed += 50
    elif command == "d":  # right
        current_left_speed -= 50

    # Limit the speed between -100 and 100
    current_left_speed = max(min(current_left_speed, 100), -100)
    current_right_speed = max(min(current_right_speed, 100), -100)

    # Set updated speeds to motors
    Lespy.setMotor(current_left_speed, current_right_speed)
    print(f"[MOVIMENTO] Velocità motore sinistro: {current_left_speed}, destro: {current_right_speed}")

def reset_movement(command):
    """
    Resets the movement when a command is released.
    """
    global current_left_speed, current_right_speed

    if command == "w":  # forward
        current_left_speed += 50
        current_right_speed -= 50
    elif command == "s":  # backward
        current_left_speed -= 50
        current_right_speed += 50
    elif command == "a":  # left
        current_right_speed -= 50
    elif command == "d":  # right
        current_left_speed += 50

    # Limit the speed between -100 and 100
    current_left_speed = max(min(current_left_speed, 100), -100)
    current_right_speed = max(min(current_right_speed, 100), -100)

    # Set updated speeds to motors
    Lespy.setMotor(current_left_speed, current_right_speed)
    print(f"[RESET] Velocità motore sinistro: {current_left_speed}, destro: {current_right_speed}")

def start_server():
    """
    Starts the server and accepts new connections.
    """
    global run_server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADD)
    server_socket.listen()
    print(f"[SERVER] In ascolto su {SERVER_ADD}...")
    Lespy.stop()

    try:
        while run_server:
            connection, client_address = server_socket.accept()
            clients.append(connection)

            # Start a thread for each connected client
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()

    except KeyboardInterrupt:
        print("[SERVER] Interruzione ricevuta, sto chiudendo il server.")
    
    # Close all connections when the server is interrupted
    for client in clients:
        client.close()

    server_socket.close()
    print("[SERVER] Chiusura completata.")

if __name__ == "__main__":
    start_server()
