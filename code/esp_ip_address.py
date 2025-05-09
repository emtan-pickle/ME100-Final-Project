import network
import time

def connect_wifi():
    print("Starting Wi-Fi connection...") 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Berkeley-IoT', 'v1+4wUMm')
    print("Waiting for connection...")
    while not wlan.isconnected():
        time.sleep(0.5)
        print("Still waiting...") #so i dont think that the system is bugging because it takes a while to get ip address
    print("Connected to WiFi")
    print("ESP32 IP address:", wlan.ifconfig()[0])
connect_wifi()