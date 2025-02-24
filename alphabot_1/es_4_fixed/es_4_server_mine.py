import time
#import alpha_bot as ab
import threading
import socket

#connection vars
MY_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

#Alphabot
##Lespy = ab.AlphaBot() controllo comando

#heartbeat vars
CHECK_INTERVAL = 5
connection_active = True
s_hb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def heartbeat_receive(receive_heartbeat):

    global connection_active

    while True:
        try: 

            ping = receive_heartbeat.recv(4092)
            print(ping)
            s_hb.settimeout(CHECK_INTERVAL)
             
        except socket.timeout:

            print("ferma tutto")
            connection_active = False
            break
        


        except Exception as e:

            print(f"exception throw: {e}")
            break

    print("si è rotto tutto")
        
def main():
    #print("start")
    """
    Autore: Danilo Rinaldi Mattia Mauro
    Data: 10/10/2024
    Server TCP monoconnessione
    """
    #setting #Lespy
    #Lespy.stop()

    s_ab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ab.bind(MY_ADDRESS)
    s_ab.listen()

    connection, client_address = s_ab.accept()
    print(f"Il client {client_address} si è connesso")

    global connection_active

    is_hb = threading.Thread(target = heartbeat_receive, args=(connection,))  # Verifica lo stato della connessione

    is_hb.start()

    while True:

        #print(connection_active)

        #print(connection_active)

        if not connection_active:
            print("Chiudo il server a causa della perdita di connessione.")
            break  # Esce dal loop se la connessione è persa

        #try:
        message = connection.recv(BUFFER_SIZE).decode()
        command, value = message.split('|')
        #print(command, value)
        #print("controllo comando")
        if command != "heartbeat":
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

        #except Exception as e:
            #print(f"Errore di connessione {e}, chiusura del server")
            #Lespy.stop()
            #break

if __name__ == '__main__':
    main()
