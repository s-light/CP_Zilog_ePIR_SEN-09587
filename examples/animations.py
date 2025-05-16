# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# based on
# https://learn.adafruit.com/circuitpython-led-animations/basic-animations#full-example-code-3063749

"""
just fadeOn to a solid color -
wait a little
and fadeOff again.
"""

import time
import board

# from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.color import (
    AMBER,
    BLACK,
)
from adafruit_led_animation.sequence import AnimateOnce

# Update to match the number of NeoPixels you have connected
pixel_num = 1

print("\n\n")
print("fade experiment")

if hasattr(board, "APA102_SCK"):
    import adafruit_dotstar
    pixels = adafruit_dotstar.DotStar(
        board.APA102_SCK, board.APA102_MOSI, pixel_num, auto_write=False
    )
else:
    import neopixel
    pixels = neopixel.NeoPixel(board.NEOPIXEL, pixel_num, auto_write=False)

pixels.brightness = 0.3

fadeOnCC = ColorCycle(pixels, speed=5, colors=[BLACK, AMBER])
fadeOffCC = ColorCycle(pixels, speed=5, colors=[AMBER, BLACK])

fadeOn = AnimateOnce(
    fadeOnCC,
    # auto_clear=False,
    # auto_reset=True,
    advance_interval=5,
)
fadeOff = AnimateOnce(
    fadeOffCC,
    # auto_clear=False,
    # auto_reset=True,
    advance_interval=5,
)


print("wait 5sec")
time.sleep(5)

print("start fadeOn:")
while fadeOn.animate():
    pass
print("done.")

print("wait 5sec")
time.sleep(5)

print("start fadeOff:")
while fadeOff.animate():
    pass
print("done.")

print("wait 10sec")
time.sleep(10)
print("done with this script. exiting.")
# while True:
#     pass
