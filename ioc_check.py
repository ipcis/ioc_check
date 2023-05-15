import csv
import requests

def is_tor_exit_node(ip_address):
    url = f"https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip={ip_address}&port=80"
    response = requests.get(url)
    return "not listed" not in response.text

def check_tor_exit_nodes(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        ip_addresses = [row[0] for row in reader]

    for ip_address in ip_addresses:
        if is_tor_exit_node(ip_address):
            print(f"{ip_address} is a Tor exit node relay.")
        else:
            print(f"{ip_address} is not a Tor exit node relay.")

# Beispielaufruf
check_tor_exit_nodes('ip_addresses.csv')
