import socket , network
from machine import Pin, PWM
from time import sleep

#NOTE: this code references an existing github repository at certain points which i will paste here: https://gist.github.com/cyrusmeh/901249c60a64eda9ae124b2d1e20cd4e

ssid = 'Berkeley-IoT' #shared wifi name
password = 'v1+4wUMm' #ESP wifi password
sta = network.WLAN(network.STA_IF) #setting ESP as a wifi station
sta.active(True) #activating ESP wifi station
sta.connect(ssid , password) #ESP connects to router thru using ssid and password
while sta.isconnected() == False : #if no wifi connection, rest of the code will be null
    pass
print('connection successful ')
print(sta.ifconfig())

servo = PWM(Pin(22), freq=50) #creating pin object called servo that is connected to gpio22 or sda on ESP

lock_state = "LOCK" #general lock state when not called upon

def set_servo_state(state): #function to define the lock state of servo and defines how much the servo will turn
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
        
def web_page(): #this variable defines the web page. we will use HTML, CSS, and JS to generate the look of the website. we use + lock_state + to send a signal to the gpio22 pin which will let the servo know whether to unlock or lock
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
        </body>
    </html>"""
    return html

# create a socket using socket.socket(), and specify the socket type. we create a new socket object called s with the given address family, and socket type. this is a STREAM TPC socket:
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# the bind() method accepts a tupple variable with the ip address, and port number:
s.bind(('' ,80))
#enables the server to accept connections; it makes a "listening" socket. the argument specifies the maximum number of queued connections. the maximum is 5.
s.listen(5)
while True:
#when a client connects, it saves a new socket object to accept and send data on the conn variable, and saves the client address to connect to the server on the addr variable.
    conn , addr = s.accept()
#the following line gets the request recieved onthe newly created socket and saves it in the request variable.
    request = conn.recv(1024)
    request = str(request)
    action_unlock = request.find('/?action=unlock')
    action_lock = request.find('/?action=lock')

    if action_unlock == 6:
        set_servo_state('unlock')

    if action_lock == 6:
        set_servo_state('lock')
        
    conn.sendall(web_page())
#in the end, close the created socket.
    conn.close()