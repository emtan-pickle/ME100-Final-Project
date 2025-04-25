from machine import UART
import time

# Initialize UART
uart = UART(2, baudrate=57600, tx=08, rx=07)

# Get Image Command
get_image_cmd = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'

def capture_fingerprint():
    print("Place your finger on the sensor...")

    for attempt in range(5):  # Try 5 times before giving up
        uart.write(get_image_cmd)
        time.sleep(1)

        if uart.any():
            response = uart.read()
            print(f"Attempt {attempt+1} - Raw Response: {response}")

            if response and response[9] == 0x00:
                print("Fingerprint captured successfully!")
                return True
            elif response and response[9] == 0x01:
                print("No finger detected.")
            elif response and response[9] == 0x02:
                print("Image too messy, try again.")
            elif response and response[9] == 0x03:
                print("Image too dry, try again.")
            else:
                print(f"Capture failed, code: {response[9]}")
        else:
            print("No response from sensor.")

        time.sleep(5)  # Give sensor time before next attempt

    print("Failed to capture fingerprint after 5 attempts.")
    return False

# Call the function
capture_fingerprint()