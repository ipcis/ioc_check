#!/usr/bin/env python3

import csv
import requests
import ipaddress
import argparse

def is_valid_ip(ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ipaddress.AddressValueError:
        return False

def is_private_ip(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return ip.is_private
    except ValueError:
        return False

def load_exit_nodes():
    url = "https://check.torproject.org/torbulkexitlist"
    response = requests.get(url)
    exit_nodes = []

    lines = response.text.split('\n')
    for line in lines:
        exit_nodes.append(line)
 
    return exit_nodes

def is_tor_exit_node(ip_address, exit_nodes):
    return ip_address in exit_nodes

def check_tor_exit_nodes(csv_file):
    exit_nodes = load_exit_nodes()

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        ip_addresses = [row[0] for row in reader]

    filtered = []
    true_iocs = []

    for ip_address in ip_addresses:
        if is_valid_ip(ip_address):
            if not is_private_ip(ip_address):
                if is_tor_exit_node(ip_address, exit_nodes):
                    filtered.append((ip_address, "Tor node"))
                    print(f"{ip_address} is a Tor exit node relay.")
                else:
                    true_iocs.append(ip_address)
            else:
                filtered.append((ip_address, "private IP"))
                print(f"{ip_address} is a private IP address and will not be checked.")
        else:
            filtered.append((ip_address, "invalid IP"))
            print(f"{ip_address} is not a valid IP address.")

    with open(f"{csv_file}_filtered", 'w') as file:
        for line in true_iocs:
            file.write(f"{line}\n")

    with open(f"{csv_file}_removed", 'w') as file:
        for line in filtered:
            file.write(f"{line[0]}\t{line[1]}\n")

# Argument parser
parser = argparse.ArgumentParser(
    prog='ioc check',
    description='Check a list of IoCs for TOR addresses',
)
parser.add_argument('ioclist')
args = parser.parse_args()

# main call
check_tor_exit_nodes(args.ioclist)
