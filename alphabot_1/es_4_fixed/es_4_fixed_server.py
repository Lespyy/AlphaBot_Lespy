import socket
import time
#import alpha_bot
import threading


#connection vars
MYADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

#Alpha bot
#Lespy = alpha_bot.AlphaBot()

#Heart Beat vars
CHECK_INTERVAL = 2  # Intervallo per il controllo della connessione (in secondi)

def stop_robot():
    """Ferma il robot."""
    #Lespy.stop()
    print("stop")

def heartbeat(connection):
    """Controlla periodicamente la connessione e ritorna False se la connessione è persa."""
    try:
        connection.send("ping".encode())  # Invia un messaggio per verificare la connessione
        time.sleep(CHECK_INTERVAL)
        return True
    except (socket.error, BrokenPipeError):
        print("Connessione persa.")
        stop_robot()  # Ferma il robot in caso di disconnessione
        return False

def main():
    """
    Autore: Danilo Rinaldi Mattia Mauro
    Data: 10/10/2024
    Server TCP monoconnessione
    """
    
    #Lespy.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    connection_active = True

    while connection_active:
        connection_active = heartbeat(connection)  # Verifica lo stato della connessione

        if not connection_active:
            print("Chiudo il server a causa della perdita di connessione.")
            break  # Esce dal loop se la connessione è persa

        try:
            message = connection.recv(BUFFER_SIZE).decode()
            command, value = message.split('|')
            print(command, value)

            if command == "forward":
                #Lespy.forward()
                print("forward")
                time.sleep(int(value))
                #Lespy.stop()

            elif command == "backward":
                #Lespy.backward()
                print("backward")
                time.sleep(int(value))
                #Lespy.stop()

            elif command == "left":
                #Lespy.left()
                print("left")
                time.sleep(int(value))
                #Lespy.stop()

            elif command == "right":
                #Lespy.right()
                print("right")
                time.sleep(int(value))
                #Lespy.stop()

            else:
                connection.send("error|Comando non riconosciuto".encode())

        except (socket.error, BrokenPipeError):
            print("Errore di connessione, chiusura del server")
            stop_robot()
            break

if __name__ == '__main__':
    main()
