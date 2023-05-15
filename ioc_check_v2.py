import csv
import requests
import socket

def is_valid_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False

def is_internal_ip(ip_address):
    # Liste der reservierten IP-Adressbereiche
    reserved_ips = [
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16'
    ]

    ip = ip_address.split('.')
    ip_value = (int(ip[0]) << 24) + (int(ip[1]) << 16) + (int(ip[2]) << 8) + int(ip[3])

    for reserved_ip in reserved_ips:
        network, prefix = reserved_ip.split('/')
        network_value = sum([int(x) << (24 - i * 8) for i, x in enumerate(network.split('.'))])
        if (ip_value & (0xFFFFFFFF << (32 - int(prefix)))) == network_value:
            return True

    return False

def is_tor_exit_node(ip_address):
    url = f"https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip={ip_address}&port=80"
    response = requests.get(url)
    return "not listed" not in response.text

def check_tor_exit_nodes(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        ip_addresses = [row[0] for row in reader]

    for ip_address in ip_addresses:
        if is_valid_ip(ip_address) and not is_internal_ip(ip_address):
            if is_tor_exit_node(ip_address):
                print(f"{ip_address} is a Tor exit node relay.")
            else:
                print(f"{ip_address} is not a Tor exit node relay.")
        else:
            print(f"{ip_address} is not a valid or internal IP address.")

# Beispielaufruf
check_tor_exit_nodes('ip_addresses.csv')
