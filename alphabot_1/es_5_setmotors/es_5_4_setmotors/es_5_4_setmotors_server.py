import socket
import threading
import time
#from alpha_bot import AlphaBot

SERVER_ADD = ("0.0.0.0", 9094)
BUFFER_SIZE = 4096

# Global variables
#Lespy = AlphaBot()
clients = []
lock = threading.Lock()

# Current motor speeds
current_left_speed = 0
current_right_speed = 0

def handle_client(connection, address):
    """
    Handles commands from a client.
    """
    global clients
    print(f"[SERVER] Client connected: {address}")
    clients.append(connection)

    try:
        while True:
            message = connection.recv(BUFFER_SIZE).decode()
            if not message:
                break

            if message == "Can you hear me?":
                print(f"[SERVER] Heartbeat from {address}")
            else:
                command, action = message.split("|")
                with lock:
                    if action == "start":
                        update_movement(command)
                    elif action == "stop":
                        reset_movement(command)
    except Exception as e:
        print(f"[SERVER] Error with {address}: {e}")
    finally:
        print(f"[SERVER] Client disconnected: {address}")
        connection.close()
        clients.remove(connection)

def heartbeat_monitor():
    """
    Monitors the connection with clients using heartbeat messages.
    """
    global clients
    while True:
        time.sleep(5)
        with lock:
            for client in clients:
                try:
                    client.sendall("Heartbeat check".encode())
                except Exception as e:
                    print(f"[SERVER] Lost connection with client: {e}")
                    clients.remove(client)

def update_movement(command):
    """
    Updates motor speeds incrementally based on commands.
    """
    global current_left_speed, current_right_speed

    # Command-to-speed mapping
    speed_increment = {"w": (-20, -20), "s": (20, 20), "a": (-10, -20), "d": (-20, -10)}
    if command in speed_increment:
        left_inc, right_inc = speed_increment[command]
        current_left_speed += left_inc
        current_right_speed += right_inc

        # Limit speeds between -100 and 100
        current_left_speed = max(min(current_left_speed, 100), -100)
        current_right_speed = max(min(current_right_speed, 100), -100)

        # Apply speeds to motors
        # Lespy.setMotor(current_left_speed, current_right_speed)
        print(f"[SERVER] Updated speeds: Left={current_left_speed}, Right={current_right_speed}")

def reset_movement(command):
    """
    Decreases motor speeds incrementally when a key is released.
    """
    global current_left_speed, current_right_speed

    speed_decrement = {"w": (20, 20), "s": (-20, -20), "a": (10, 20), "d": (20, 10)}
    if command in speed_decrement:
        left_dec, right_dec = speed_decrement[command]
        current_left_speed += left_dec
        current_right_speed += right_dec

        # Limit speeds between -100 and 100
        current_left_speed = max(min(current_left_speed, 100), -100)
        current_right_speed = max(min(current_right_speed, 100), -100)

        # Apply speeds to motors
        # Lespy.setMotor(current_left_speed, current_right_speed)
        print(f"[SERVER] Reset speeds: Left={current_left_speed}, Right={current_right_speed}")

def start_server():
    """
    Starts the server and accepts new connections.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(SERVER_ADD)
    server_sock.listen()
    print("[SERVER] Listening...")

    # Start heartbeat monitor in a separate thread
    threading.Thread(target=heartbeat_monitor, daemon=True).start()

    try:
        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("[SERVER] Shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    #Lespy.stop()
    start_server()
