#!/usr/bin/env python

import scapy.all as scapy

def sniff_packets(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed)

def process_sniffed(packet):
    if packet.hasLayer[scapy.ARP] and packet[scapy.ARP].op == 2:
        try:
            # Asking for the real Mac correspondent to this IP
            true_mac = get_mac_from_ip(packet[scapy.ARP].psrc)
            # Getting the MAC from the reponse
            current_mac = packet[scapy.ARP].hwsrc
            # If it differs, we are under attack
            if true_mac != current_mac:
                print("UNDER ATTACK!!!")
        except IndexError:
            pass

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
