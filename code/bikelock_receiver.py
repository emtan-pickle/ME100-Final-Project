import time
import espnow
from machine import PWM, Pin
import network

#esp now initialize
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.config(channel=1)
e = espnow.ESPNow()
e.active(True)



servo = PWM(Pin(22), freq=50)

# lock/unlock servo
def set_servo_state(state):
    if state == 'unlock':
        servo.duty(77)  # Adjust duty for 'unlock', e.g., 2ms pulse (~12.5% duty)
        print("Unlocked")
    elif state == 'lock':
        servo.duty(40)  # Adjust duty for 'lock', e.g., 1ms pulse (~5% duty)
        print("Locked")

# receive commands from esp32
while True:
    message = e.recv()
    if message:
        if len(message) == 2:
            mac, raw_data = message
        else:
            raw_data = message[0]
        try:
            command = raw_data.decode('utf-8')  # <-- Correct decoding target
            print("Received command:", command)
            set_servo_state(command)
        except UnicodeError:
            print("Received non-UTF-8 data:", raw_data)
    time.sleep(1)