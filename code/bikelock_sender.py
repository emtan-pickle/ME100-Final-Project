import time
import espnow
from machine import Pin
import network

#esp now set up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
espnow.init()

#mac address of receiver
receiver_mac = b'\x24\x6F\x28\x89\x5D\xA1'

servo_pin = Pin(19, Pin.OUT)

def send_message(message):
    espnow.send(receiver_mac, message)
    
while True:
    command = input("Enter command (unlock/lock): ")  # Input for unlock/lock
    send_message(command)
    print("Message sent:", command)
    time.sleep(2)