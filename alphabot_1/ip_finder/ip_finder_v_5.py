import socket
from scapy.all import *

# Funzione per trovare IP e nome del dispositivo
def get_device_name(ip):
    try:
        name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        name = "Nome non risolto"
    return name

# Funzione per trovare le porte aperte
def scan_ports(ip, port_range=(1, 1024)):
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        tcp_packet = IP(dst=ip) / TCP(dport=port, flags="S")
        response = sr1(tcp_packet, timeout=0.5, verbose=0)
        if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
            open_ports.append(port)
            sr1(IP(dst=ip) / TCP(dport=port, flags="R"), timeout=0.5, verbose=0)
    return open_ports

# Lista degli IP della rete da scansionare
network_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]  # Sostituisci con gli IP della tua rete

# Scansione della rete
for ip in network_ips:
    device_name = get_device_name(ip)
    open_ports = scan_ports(ip)
    print(f"IP: {ip}")
    print(f"Nome Dispositivo: {device_name}")
    print(f"Porte Aperte: {open_ports}")
    print("----------")
