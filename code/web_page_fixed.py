import socket
import network
import espnow
from machine import Pin, PWM
from time import sleep

# --------------------------
# Set ESP32 as Access Point
# --------------------------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='JEMs-Bike-Lock', password='supersecretpassword123', authmode=network.AUTH_WPA2_PSK)

while not ap.active():
    pass

print('Access Point ready')
print('Connect to: JEMs-Bike-Lock')
print('Password: supersecretpassword123')
print('Go to: http://192.168.4.1')

e = espnow.ESPNow()
e.init()
tamper_status = False
# --------------------------
# Servo Setup
# --------------------------
servo = PWM(Pin(22), freq=50)
lock_state = "LOCK"

def tamper_check():
    global tamper_status
    if e.poll():
        peer, msg = e.recv()
        if msg = b"tamper":
            print("There is tampering on your lock!")
            tamper_status = True
def set_servo_state(state):
    global lock_state
    if state == 'unlock':
        servo.duty(102)
        lock_state = "UNLOCK"
        print("Unlocked")
        sleep(0.5)
    elif state == 'lock':
        servo.duty(51)
        lock_state = "LOCK"
        print("Locked")
        sleep(0.5)

# --------------------------
# Web Page (exact styling from your code)
# --------------------------
def web_page():
    html = """<html>
        <head>
            <title>JEM's Very Secure and Awesome and Cool and the Best Bike Lock 🚲🔒</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style>
                html {
                    font-family: 'Comic Sans MS', 'Roboto Mono', cursive;
                    background: #FFF5F9;
                    color: #444;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    color: #FF92A5;
                    font-size: 2.5em;
                    margin-top: 3vh;
                }
                p {
                    font-size: 1.4rem;
                    color: #555;
                }
                .button {
                    background-color: #A8DADC;
                    border: none;
                    border-radius: 12px;
                    color: #1D3557;
                    padding: 14px 36px;
                    font-size: 1.2rem;
                    font-weight: bold;
                    cursor: pointer;
                    margin: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
                }
                .button:hover {
                    background-color: #74C69D;
                    transform: scale(1.05);
                }
                .button2 {
                    background-color: #FFD6A5;
                    color: #6A4C93;
                }
                .button2:hover {
                    background-color: #FFB5A7;
                }
                strong {
                    color: #FF8FAB;
                    font-size: 1.6rem;
                }
                .container {
                    padding: 3vh;
                    max-width: 600px;
                    margin: auto;
                    background-color: #FDFCDC;
                    border-radius: 20px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.1);
                }
                .typewriter-container {
                    margin-top: 2vh;
                    font-family: 'Courier New', monospace;
                    font-size: 1.5rem;
                    color: #6A4C93;
                    min-height: 2em;
                    white-space: nowrap;
                    overflow: hidden;
                    border-right: 2px solid #6A4C93;
                    width: fit-content;
                    margin-left: auto;
                    margin-right: auto;
                    animation: blink-caret 0.75s step-end infinite;
                }
                @keyframes blink-caret {
                    from, to { border-color: transparent }
                    50% { border-color: #6A4C93; }
                }
            </style>
        </head>
        <body>
            <div class="container">
              <h1>🌸 JEM's Super Awesome and Cool Bike Lock That is Better Than All the Other Ones 🌸</h1>
              <p>🔐 Lock Status: <strong>""" + lock_state + """</strong></p>
              <p><a href="/?action=unlock"><button class="button">✨ Unlock ✨</button></a></p>
              <p><a href="/?action=lock"><button class="button button2">🧸 Lock 🧸</button></a></p>
            </div>
            <div class="typewriter-container">
              <span id="typewriter-text"></span>
            </div>
            <script>
              const lockState = `""" + lock_state + """`;
              const message = lockState === "LOCK" 
                  ? "Your bike lock is secure 🔒"
                  : "Your bike lock is unsecured 🔓";
              const textElem = document.getElementById("typewriter-text");
              let index = 0;
              function typeWriter() {
                if (index < message.length) {
                    textElem.textContent += message.charAt(index);
                    index++;
                    setTimeout(typeWriter, 75);
                }
              }
              window.onload = typeWriter;
            </script>
            if tamper_status:
                html += "<p style='color:red; font-size:1.5em;'>🚨 TAMPERING DETECTED!</p>"
        </body>
    </html>"""
    return html

# --------------------------
# Web Server Loop
# --------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Client connected from:', addr)
    request = conn.recv(1024)
    request = str(request)

    if '/?action=unlock' in request:
        set_servo_state('unlock')
    elif '/?action=lock' in request:
        set_servo_state('lock')
    
    check_for_tamper()
    conn.sendall(web_page())
    conn.close()
