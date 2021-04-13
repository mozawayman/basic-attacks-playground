#!/usr/bin/env python
import subprocess
import optparse ## command line arguments
import re

def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Interface to change MAC Address")
    parse.add_option("-m", "--mac", dest="new_mac", help="New Mac")
    (options, arguments) = parse.parse_args()
    if not options.interface:
        parse.error("Please Provide interface")
    if not options.new_mac:
        parse.error("Please Provide New_Mac address")
    return options

def mac_changer(interface, new_mac):
    print("Changing interface for " + interface + " to : " + new_mac)
    ##List version prevents hijack with semi-colons
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac_address(interface):
    ifconfigOutput = subprocess.check_output(["ifconfig", interface])
    actual_mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w', ifconfigOutput)
    if actual_mac_address:
        return actual_mac_address.group(0)
    else:
        print("ERROR Could not read MAC")

options = get_arguments()
currentMac = get_current_mac_address(options.interface)
print(currentMac)

mac_changer(options.interface, options.new_mac)

currentMac = get_current_mac_address(options.interface)
if currentMac == options.new_mac:
    print("Success Mac changed to: " + currentMac)
else:
    print("Fail Mac didn't change ")


