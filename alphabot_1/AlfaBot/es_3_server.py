import socket
import time
import alpha_bot
diz_command = {"forward" : "avanti", "backward" : "indietro", "left" : "sinistra", "right": "destra"} #lista di comandi

MYADDRESS = ("192.168.1.138", 9090)
BUFFER_SIZE = 4096

def main():
    """
    Author: Rinaldi Danilo & Mauro Mattia
    date: 19/09/2024
    es.server TCP
    text: fare un server TCP che gestisca un solo client, monoconnessione
    """
	
    Lespy = alpha_bot.AlphaBot()
    Lespy.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    while True:
        
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

        if phrase == "avanti":
            Lespy.forward()
            time.sleep(int(value))
            Lespy.stop()
        
        elif phrase == "indietro":
            Lespy.backward()
            time.sleep(int(value))
            Lespy.stop()

        elif phrase == "sinistra":
            Lespy.left()
            time.sleep(int(value))
            Lespy.stop()

        elif phrase == "destra":
            Lespy.right()
            time.sleep(int(value))
            Lespy.stop()

        elif phrase == "avanti" and phrase == "destra":
            Lespy.forward()
            Lespy.right()
            time.sleep(value)
            Lespy.stop()

        elif phrase == "avanti" and phrase == "sinistra":
            Lespy.forward()
            Lespy.left()
            time.sleep(value)
            Lespy.stop()
            
        elif phrase == "indietro" and phrase == "sinistra":
            Lespy.backward()
            Lespy.left()
            time.sleep(value)
            Lespy.stop()

        elif phrase == "indietro" and phrase == "deatra":
            Lespy.backward()
            Lespy.right()
            time.sleep(value)
            Lespy.stop()
        
                   
if __name__ == '__main__':
    main()