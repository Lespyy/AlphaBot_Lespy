import asyncio
import os
import socket

async def ping(ip):
    """Ping a specific IP address and return the IP if reachable."""
    command = f"ping -n 1 -w 1 {ip}" if os.name == "nt" else f"ping -c 1 -W 1 {ip}"
    
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return ip if proc.returncode == 0 else None

async def resolve_hostname(ip):
    """Resolve the hostname for a given IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

async def scan_network(network_prefix):
    """Scan the network for active IP addresses and resolve their hostnames."""
    # Ping all addresses in the subnet
    tasks = [ping(f"{network_prefix}.{i}") for i in range(1, 255)]
    results = await asyncio.gather(*tasks)
    active_ips = [ip for ip in results if ip]
    
    # Resolve hostnames for active IPs
    resolve_tasks = [resolve_hostname(ip) for ip in active_ips]
    hostnames = await asyncio.gather(*resolve_tasks)
    
    return list(zip(active_ips, hostnames))

if __name__ == "__main__":
    # Modifica il prefisso della rete in base alla tua configurazione
    network_prefix = "192.168.188"
    
    print(f"Scansione della rete {network_prefix}.0/24 in corso...")
    results = asyncio.run(scan_network(network_prefix))
    
    print("\nDispositivi trovati:")
    for ip, hostname in results:
        print(f"IP: {ip}, Hostname: {hostname}")
