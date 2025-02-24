import socket
import threading
#from alpha_bot import AlphaBot

SERVER_ADD = ("0.0.0.0", 9091)
BUFFER_SIZE = 4096

# Global variables
#Lespy = AlphaBot()
clients = []
lock = threading.Lock()

def handle_client(connection, address):
    """
    Handles commands from a client.
    """
    print(f"[SERVER] Client connected: {address}")
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

def update_movement(command):
    """
    Updates motor speeds based on commands.
    """
    speeds = {"w": (-50, -50), "s": (50, 50), "a": (-25, -50), "d": (-50, -25)}
    if command in speeds:
        left, right = speeds[command]
        #Lespy.setMotor(left, right)
        print(f"[SERVER] Command {command}: Left={left}, Right={right}")

def reset_movement(command):
    """
    Resets the motors when keys are released.
    """
    #Lespy.setMotor(0, 0)
    print(f"[SERVER] Reset movement for command {command}")

def start_server():
    """
    Starts the server.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(SERVER_ADD)
    server_sock.listen()
    print("[SERVER] Listening...")

    try:
        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("[SERVER] Shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    #Lespy.stop()
    start_server()
