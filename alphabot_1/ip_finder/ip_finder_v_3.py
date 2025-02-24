import scapy.all as scapy
import socket
import threading

def get_ip_range():
    """Gets the IP range of the local network based on your IP address"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'  # Default range for most networks
    return ip_range

def scan(ip_range):
    """Scans the network and returns a list of devices with their IP and MAC address"""
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=0.5, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    
    return devices

def resolve_hostname(device):
    """Resolves the hostname of a device"""
    try:
        device['hostname'] = socket.gethostbyaddr(device['ip'])[0]
    except socket.herror:
        device['hostname'] = "Unknown"

def print_devices(devices):
    """Prints the list of devices with IP, MAC, and hostname"""
    print("Available devices on the network:")
    print("IP\t\t\tMAC Address\t\t\tHostname")
    print("-" * 70)
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}\t\t{device['hostname']}")

# Main code
if __name__ == "__main__":
    ip_range = get_ip_range()
    devices = scan(ip_range)

    threads = []
    for device in devices:
        thread = threading.Thread(target=resolve_hostname, args=(device,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print_devices(devices)
