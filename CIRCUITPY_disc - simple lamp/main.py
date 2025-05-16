# SPDX-FileCopyrightText: 2025 Stefan Krüger
#
# SPDX-License-Identifier: MIT
#
# based on
# https://learn.adafruit.com/introducing-adafruit-itsybitsy-m4/circuitpython-internal-rgb-led
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial

"""CircuitPython Zilog ePir SEN-09587 example"""
import time
import board
import busio
import digitalio

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import RED

import nonblocking_serialinput as nb_serial

print("\n")
print("CircuitPython Essentials Internal RGB LED red, green, blue example")


if hasattr(board, "APA102_SCK"):
    print("APA102")
    import adafruit_dotstar
    led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    print("NEOPIXEL")
    import neopixel
    led = neopixel.NeoPixel(board.NEOPIXEL, 1)

led.brightness = 0.0
led[0] = (255, 100, 0)


uart = busio.UART(board.TX, board.RX, baudrate=9600)


my_input = nb_serial.NonBlockingSerialInput(
    # input_handling_fn=userinput_event_handling,
    # print_help_fn=userinput_print_help,
    # echo=True,
)

my_input.print("enable motion report...")
uart.write('M')
time.sleep(0.01)
uart.write('Y')
time.sleep(0.01)
my_input.print("done.")

def fadeOn():
    my_input.print("fadeOn")
    for i in range(0, 1000):
        led.brightness = i/1000
        time.sleep(0.01)
    my_input.print("fadeOn done.")

def fadeOff():
    my_input.print("fadeOff")
    for i in range(1000, 0, -1):
        led.brightness = i/1000
        time.sleep(0.02)
    my_input.print("fadeOff done.")

def waitForSensorReady():
    ready = False
    while not ready:
        uart.write('a')
        if (uart.read(1) is not b'U'):
            ready = True
            time.sleep(1)


# ##########################################
# main

led.brightness = 0.1
led[0] = (50, 0, 255)

waitForSensorReady()

led.brightness = 0.0
led[0] = (255, 100, 0)

while True:
    while uart.in_waiting > 0:
        sensorInput = uart.read(1)
        if sensorInput == b'M':
            my_input.print("Motion!")
            # led.brightness = 1.0
            fadeOn()
            time.sleep(20)
            fadeOff()
            uart.reset_input_buffer()
        else:
            my_input.print(sensorInput)  # this is a bytearray type

    my_input.update()
    input_string = my_input.input()
    if input_string is not None:
        uart.write(input_string)
