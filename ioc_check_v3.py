import csv
import requests
import socket

def is_valid_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False

def load_exit_nodes():
    url = "https://check.torproject.org/exit-addresses"
    response = requests.get(url)
    exit_nodes = []

    lines = response.text.split('\n')
    for line in lines:
        if line.startswith('ExitAddress'):
            parts = line.split(' ')
            if len(parts) >= 2:
                exit_nodes.append(parts[1])

    return exit_nodes

def is_tor_exit_node(ip_address, exit_nodes):
    return ip_address in exit_nodes

def check_tor_exit_nodes(csv_file):
    exit_nodes = load_exit_nodes()

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        ip_addresses = [row[0] for row in reader]

    for ip_address in ip_addresses:
        if is_valid_ip(ip_address):
            if is_tor_exit_node(ip_address, exit_nodes):
                print(f"{ip_address} is a Tor exit node relay.")
            else:
                print(f"{ip_address} is not a Tor exit node relay.")
        else:
            print(f"{ip_address} is not a valid IP address.")

# Beispielaufruf
check_tor_exit_nodes('ip_addresses.csv')
