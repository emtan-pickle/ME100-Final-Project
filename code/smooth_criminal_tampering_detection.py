from machine import I2C, Pin, PWM
import time

# ——— USER CONFIG ———
I2C_BUS             = 1       # I2C peripheral number
I2C_SCL_PIN         = 20      # GPIO pin for SCL
I2C_SDA_PIN         = 22      # GPIO pin for SDA
BUZZER_PIN          = 14      # GPIO pin for buzzer
LSM6DSO_ADDR        = 0x6B    # IMU I2C address (SA0 tied to VCC)
CALIBRATION_SAMPLES = 200      # Number of samples for baseline
TAMPER_THRESHOLD    = 5000     # Delta threshold for tamper detection
CONSECUTIVE_COUNT   = 3        # Readings above threshold to confirm
COOLDOWN_MS         = 2000     # Lockout period after melody (ms)
DEBUG               = False    # Set True to print delta values
# ———————————————————

# ——— LSM6DSO REGISTER MAP ———
_REG_WHO_AM_I       = 0x0F
_REG_CTRL1_XL       = 0x10
_REG_CTRL2_G        = 0x11
_REG_OUTX_L_XL      = 0x28  # First of 6 accel data bytes
# ————————————————————————

# Initialize I2C bus and buzzer
i2c = I2C(I2C_BUS, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(1000)
buzzer.duty(0)

# Improved frequency mapping for "Smooth Criminal" riff
NOTES = {
    'A4': 440,
    'B4': 494,
    'C#5': 554,
    'D5': 587,
    'E5': 659,
    'F#5': 740,
}

# More recognizable "Smooth Criminal" opening riff
MELODY = [
    ('C#5', 100), ('C#5', 100), ('C#5', 100), ('C#5', 100),
    ('F#5', 200), ('F#5', 200),
    ('E5', 200), ('D5', 200),
    ('C#5', 400),
    # Repeat phrase for effect
    ('C#5', 100), ('C#5', 100), ('C#5', 100), ('C#5', 100),
    ('F#5', 200), ('F#5', 200),
    ('E5', 200), ('D5', 200),
    ('C#5', 400),
]


def init_imu():
    who = i2c.readfrom_mem(LSM6DSO_ADDR, _REG_WHO_AM_I, 1)[0]
    if who != 0x6C:
        raise RuntimeError(f"IMU not detected (WHO_AM_I=0x{who:02X})")
    i2c.writeto_mem(LSM6DSO_ADDR, _REG_CTRL1_XL, bytes([0x40]))
    i2c.writeto_mem(LSM6DSO_ADDR, _REG_CTRL2_G,  bytes([0x40]))


def read_accel_raw():
    data = i2c.readfrom_mem(LSM6DSO_ADDR, _REG_OUTX_L_XL, 6)
    x = int.from_bytes(data[0:2], 'little', True)
    y = int.from_bytes(data[2:4], 'little', True)
    z = int.from_bytes(data[4:6], 'little', True)
    return x, y, z


def calibrate_baseline(samples):
    sx = sy = sz = 0
    for _ in range(samples):
        x, y, z = read_accel_raw()
        sx += x; sy += y; sz += z
        time.sleep_ms(5)
    return sx // samples, sy // samples, sz // samples


def play_smooth_criminal():
    """Play the Smooth Criminal opening riff."""
    for note, duration in MELODY:
        buzzer.freq(NOTES[note])
        buzzer.duty(512)
        time.sleep_ms(duration)
        buzzer.duty(0)
        time.sleep_ms(50)


def main():
    print("Initializing IMU...")
    init_imu()

    print(f"Calibrating baseline ({CALIBRATION_SAMPLES} samples)...")
    x0, y0, z0 = calibrate_baseline(CALIBRATION_SAMPLES)
    print(f"Baseline set: x={x0}, y={y0}, z={z0}")

    consec = 0
    last_play = time.ticks_ms()
    print("Monitoring for tampering...")

    while True:
        x, y, z = read_accel_raw()
        dx = x - x0; dy = y - y0; dz = z - z0

        now = time.ticks_ms()
        if abs(dx) > TAMPER_THRESHOLD or abs(dy) > TAMPER_THRESHOLD or abs(dz) > TAMPER_THRESHOLD:
            consec += 1
        else:
            consec = 0

        if consec >= CONSECUTIVE_COUNT and time.ticks_diff(now, last_play) >= COOLDOWN_MS:
            print("Smooth Criminal riff!")
            play_smooth_criminal()
            last_play = now
            consec = 0

        time.sleep_ms(100)

if __name__ == '__main__':
    main()
