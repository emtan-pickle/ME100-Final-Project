import time
import espnow
from machine import Pin
import network

#esp now initialize
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
espnow.init()

servo = Pin(21, Pin.OUT)

# lock/unlock servo
def set_servo_state(state):
    if state == 'unlock':
        servo.on()
        print("Unlocked")
    elif state == 'lock':
        servo.off()
        print("Locked")

# receive commands from esp32
while True:
    message = espnow.recv()
    if message:
        command = message[0].decode('utf-8')
        print("Received command:", command)
        set_servo_state(command)
    time.sleep(1)