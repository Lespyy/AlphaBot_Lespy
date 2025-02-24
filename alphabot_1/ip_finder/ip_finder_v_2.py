import scapy.all as scapy
import socket

def get_ip_range():
    """Gets the IP range of the local network based on your IP address"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'  # Default range for most networks
    return ip_range

def scan(ip_range):
    """Scans the network and returns a list of devices with their IP, MAC address, and hostname"""
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        try:
            hostname = socket.gethostbyaddr(element[1].psrc)[0]  # Resolve hostname
        except socket.herror:
            hostname = "Unknown"  # If hostname not found, set as Unknown
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc, 'hostname': hostname})
    
    return devices

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
    print_devices(devices)
