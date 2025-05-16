# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial

"""CircuitPython UART Serial example"""
import board
import busio
import digitalio

import nonblocking_serialinput as nb_serial


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=9600)

my_input = nb_serial.NonBlockingSerialInput(
    # input_handling_fn=userinput_event_handling,
    # print_help_fn=userinput_print_help,
    # echo=True,
)



###########################################
my_input.print("CircuitPython Essentials UART Serial example")

while True:
    while uart.in_waiting > 0 :
        hwIN = uart.read(uart.in_waiting)
        my_input.print(hwIN)  # this is a bytearray type

    # if data is not None:
    #     led.value = True

    #     # convert bytearray to string
    #     data_string = "".join([chr(b) for b in data])
    #     my_input.print(data_string, end="")

    #     led.value = False

    my_input.update()
    input_string = my_input.input()
    if input_string is not None:
        uart.write(input_string)
