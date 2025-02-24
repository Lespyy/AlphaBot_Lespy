import requests
import threading

def send_requests(url, n_requests):
    for _ in range(n_requests):
        try:
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# URL del dispositivo nella rete locale da testare
url = f"http://{input("give me the host ip")}" # Sostituisci con l'indirizzo IP del dispositivo
#url = "http://192.168.1.10"  # Sostituisci con l'indirizzo IP del dispositivo
n_threads = 10  # Numero di thread per simulare richieste simultanee
n_requests_per_thread = 100  # Numero di richieste per ogni thread

# Creazione e avvio dei thread
threads = []
for _ in range(n_threads):
    thread = threading.Thread(target=send_requests, args=(url, n_requests_per_thread))
    threads.append(thread)
    thread.start()

# Attesa della conclusione di tutti i thread
for thread in threads:
    thread.join()


