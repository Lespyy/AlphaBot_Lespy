import scapy.all as scapy
import socket
from concurrent.futures import ThreadPoolExecutor
import time

def get_ip_range():
    """Gets the IP range of the local network based on the IP address and subnet mask."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_range = local_ip.rsplit('.', 1)[0] + '.0/24'  # Default to /24 subnet
    return ip_range

def scan_network(ip_range):
    """Scans the network and returns a list of devices with their IP and MAC addresses."""
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1.5, verbose=False)[0]

    return [{'ip': element[1].psrc, 'mac': element[1].hwsrc} for element in answered_list]

def resolve_hostname(device, cache, timeout=1.5):
    """Attempts to resolve the hostname of a device by its IP address, with a timeout and cache."""
    ip = device['ip']
    
    # Check cache first
    if ip in cache:
        device['hostname'] = cache[ip]
    else:
        try:
            # Increase socket timeout for better reliability
            socket.setdefaulttimeout(timeout)
            device['hostname'] = socket.gethostbyaddr(ip)[0]
            cache[ip] = device['hostname']
        except socket.herror:
            device['hostname'] = "Unknown"
            cache[ip] = "Unknown"
        finally:
            socket.setdefaulttimeout(None)  # Reset timeout

    return device

def print_devices(devices):
    """Prints the list of devices with IP, MAC, and hostname."""
    print("Available devices on the network:")
    print("IP Address\t\tMAC Address\t\t\tHostname")
    print("-" * 70)
    for device in devices:
        print(f"{device['ip']}\t\t{device['mac']}\t\t{device['hostname']}")

if __name__ == "__main__":
    ip_range = get_ip_range()
    devices = scan_network(ip_range)
    cache = {}

    # Resolving hostnames using ThreadPoolExecutor for efficient threading
    with ThreadPoolExecutor(max_workers=10) as executor:
        devices = list(executor.map(lambda d: resolve_hostname(d, cache), devices))

    print_devices(devices)
