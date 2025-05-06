from machine import Pin, I2C, PWM
import time, math
from lsm6dso import LSM6DSO

# pin setup …
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
imu = LSM6DSO(i2c)    # use your LSM6DSO driver

alpha = 0.9
fx = fy = fz = 0.0
TAMPER_THRESH = 0.4

while True:
    # get raw accel
    ax, ay, az = imu.acceleration

    # low-pass -> gravity
    fx = alpha*fx + (1-alpha)*ax
    fy = alpha*fy + (1-alpha)*ay
    fz = alpha*fz + (1-alpha)*az

    # high-pass -> vibration
    dx = ax - fx
    dy = ay - fy
    dz = az - fz

    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    tamper = mag > TAMPER_THRESH

    # drive LEDs & buzzer as before…
    # …
    time.sleep_ms(10)
