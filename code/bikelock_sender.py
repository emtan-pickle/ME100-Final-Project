import time
import espnow
from machine import Pin
import network

#esp now set up
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.config(channel=1)
e = espnow.ESPNow()
e.active(True)



#mac address of receiver
receiver_mac = b'\x14\x2b\x2f\xaf\x5a\x80'
e.add_peer(receiver_mac)
servo_pin = Pin(22, Pin.OUT)

def send_message(message):
    e.send(receiver_mac, message)
    
while True:
    command = input("Enter command (unlock/lock): ")  # Input for unlock/lock
    send_message(command)
    print("Message sent:", command)
    time.sleep(2)