import socket
import time

diz_command = {"forward" : "avanti", "backward" : "indietro", "left" : "sinistra", "right": "destra"} #lista di comandi

MYADDRESS = ("192.168.1.138", 9090)
BUFFER_SIZE = 4096

def main():
    """
    Author: Noemi Baruffolo
    date: 19/09/2024
    es.server TCP
    text: fare un server TCP che gestisca un solo client, monoconnessione
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    while True:
        connection, client_address = s.accept()
        print(f"Il client {client_address} si è connesso")
        message = connection.recv(BUFFER_SIZE).decode()
        command, value = message.split('|')
        print(command,value)
        if command in diz_command:
            status = "okay"
            phrase = diz_command[command] 
        else:
            status = "error"  
            phrase = "comando non trovato" 
        answer = f"{status}|{phrase}"
        connection.send(answer.encode())
                   
if __name__ == '__main__':
    main()