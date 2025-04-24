import time
import espnow
from machine import Pin
import network

#esp now set up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
e = espnow.ESPNow()
e.active(True)



#mac address of receiver
receiver_mac = b'\x14\x2b\x2f\xaf\x5a\x80'

servo_pin = Pin(19, Pin.OUT)

def send_message(message):
    e.send(receiver_mac, message)
    
while True:
    command = input("Enter command (unlock/lock): ")  # Input for unlock/lock
    send_message(command)
    print("Message sent:", command)
    time.sleep(2)