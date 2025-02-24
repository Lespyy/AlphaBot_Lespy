import sqlite3
import socket
import threading
import time
from alpha_bot import AlphaBot

SERVER_ADD = ("0.0.0.0", 9094)
BUFFER_SIZE = 4096

# Global variables
Lespy = AlphaBot()
current_client = None
lock = threading.Lock()

# Current motor speeds
current_left_speed = 0
current_right_speed = 0


def handle_client(connection, address):
    """
    Handles commands from a single client.
    """
    global current_client
    print(f"[SERVER] Client connected: {address}")
    current_client = connection

    try:
        while True:
            message = connection.recv(BUFFER_SIZE).decode()
            if not message:
                break

            if message == "Can you hear me?":
                print(f"[SERVER] Heartbdeat from {address}")
            else:
                command, action = message.split("|")
                with lock:
                    if action == "start":
                        if command in ["w", "a", "s", "d"]:
                            update_movement(command)
                        else:
                            execute_special_command(command)
                    elif action == "stop":
                        if command in ["w", "a", "s", "d"]:
                            reset_movement(command)
    except Exception as e:
        print(f"[SERVER] Error with {address}: {e}")
    finally:
        print(f"[SERVER] Client disconnected: {address}")
        connection.close()
        current_client = None


def execute_special_command(command):
    """
    Executes a special command if it exists in the database.
    """
    db_name = "commands.db"

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT actions FROM commands WHERE command = ?", (command,))
            result = cursor.fetchone()

            if result:
                actions = result[0].split(",")  # Assume actions are stored as comma-separated values
                print(f"[SERVER] Executing special command '{command}': {actions}")
                for action in actions:
                    update_movement(action.strip())
                    time.sleep(0.5)  # Add delay to simulate execution of each action
                reset_movement("")  # Stop all motors after executing actions
            else:
                print(f"[SERVER] Command '{command}' not found in database.")
    except sqlite3.Error as e:
        print(f"[SERVER] Database error: {e}")


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
        Lespy.setMotor(current_left_speed, current_right_speed)
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
        Lespy.setMotor(current_left_speed, current_right_speed)
        print(f"[SERVER] Reset speeds: Left={current_left_speed}, Right={current_right_speed}")


def start_server():
    """
    Starts the server and accepts a single client connection at a time.
    """
    global current_client
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(SERVER_ADD)
    server_sock.listen()
    print("[SERVER] Listening for a single client...")

    try:
        while True:
            conn, addr = server_sock.accept()
            if current_client is None:
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            else:
                print("[SERVER] Another client tried to connect, but a session is already active.")
                conn.close()
    except KeyboardInterrupt:
        print("[SERVER] Shutting down.")
    finally:
        server_sock.close()


if __name__ == "__main__":
    Lespy.stop()
    start_server()
