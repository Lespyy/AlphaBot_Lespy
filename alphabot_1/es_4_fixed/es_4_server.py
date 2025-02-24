import time
import threading
import socket

# Connection vars
MY_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

# Alphabot (commentato per ora)
# Lespy = ab.AlphaBot()

# Heartbeat vars
CHECK_INTERVAL = 2
connection_active = True
s_hb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def heartbeat_receive(receive_heartbeat):
    global connection_active
    s_hb.settimeout(CHECK_INTERVAL)

    while True:
        try:
            ping = receive_heartbeat.recv(4092)
        except socket.timeout:
            print("Heartbeat timeout, stopping everything.")
            connection_active = False
            break
        except Exception as e:
            print(f"Exception occurred: {e}")
            break

def main():
    print("Server started.")
    """
    Autore: Danilo Rinaldi Mattia Mauro
    Data: 10/10/2024
    Server TCP monoconnessione
    """

    # Alphabot setup (commentato per ora)
    # Lespy.stop()

    s_ab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ab.bind(MY_ADDRESS)
    s_ab.listen(1)

    connection, client_address = s_ab.accept()
    print(f"Client {client_address} connected.")

    global connection_active

    while connection_active:
        # Start heartbeat check thread
        hb_thread = threading.Thread(target=heartbeat_receive, args=(connection,))
        hb_thread.start()

        if not connection_active:
            print("Server closing due to connection loss.")
            break  # Exit loop if connection is lost

        try:
            message = connection.recv(BUFFER_SIZE).decode()
            if not message:  # Connection closed by client
                print("Connection closed by client.")
                break
            if '|' not in message and 'heartbeat' not in message:  # Check if message is in correct format
                print(f"Invalid command received: {message}")
                continue

            command, value = message.split('|')
            print(f"Received command: {command} with value: {value}")

            if command == "forward":
                print("Moving forward.")
                time.sleep(float(value))

            elif command == "backward":
                print("Moving backward.")
                time.sleep(float(value))

            elif command == "left":
                print("Turning left.")
                time.sleep(float(value))

            elif command == "right":
                print("Turning right.")
                time.sleep(float(value))

            else:
                connection.send("error|Command not recognized".encode())

        except Exception as e:
            print(f"Connection error: {e}")
            break

    # Close the connection
    connection.close()
    s_ab.close()

if __name__ == '__main__':
    main()
