#!/usr/bin/env python

import scapy.all as scapy
import argparse as pars

def get_iprange_as_argument():
    parse = pars.ArgumentParser()
    parse.add_argument("-t", "--target", dest="target_ip_range", help="Ip range to scan")
    options = parse.parse_args()
    if not options.target_ip_range:
        parse.error("target_ip_range")
    return options

def create_arp(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    macipmapping = {each_answered[1].psrc : each_answered[1].hwsrc for each_answered in answered_list}
    return macipmapping

def print_table(mac_ip_mapping):
    print("IP\t\tMAC ADDRESS")
    print("_____________________________________________________\n")
    for k, v in mac_ip_mapping.items():
        print(k + "\t" + v)
    print("\n")

ip_range = get_iprange_as_argument()
print_table(create_arp(ip_range.target_ip_range))
