"""
    Code adapted from the following sources:
    MACROPAD Hotkey (https://learn.adafruit.com/macropad-hotkeys/project-code)
    Pico Four Keypad  (https://learn.adafruit.com/pico-four-key-macropad/code-the-four-keypad)
    # SPDX-FileCopyrightText: 2021 Pierre Constantineau
    # SPDX-License-Identifier: MIT
    # Raspberry Pi Pico 4x4 Macropad
"""
import board
import keypad
import time
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_itertools import cycle

# Setup palette iterator and mode
mode = 0
jade = (0, 255, 40)
magenta= (255, 0, 20)
mode_color = {0: jade, 1: magenta}
palette = ((80, 141, 184), (51, 105, 153), (120, 65, 159), (164, 41, 145),
           (205, 80, 171), (236, 117, 190), (249, 172, 93), (251, 206, 136), (252, 236, 176))
palette_iterator = cycle(palette)
# Setup neopixel, turn to green
pixel = neopixel.NeoPixel(board.GP28, 1)
pixel.brightness=0.5
pixel.fill(mode_color[mode])

kpd = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kpd)

# define keys for 4x4 v2
keys = keypad.Keys(
    pins=(  board.GP3, board.GP4,  board.GP21, board.GP22,
            board.GP6, board.GP5,  board.GP20, board.GP19,
            board.GP7, board.GP8,  board.GP17, board.GP18,
            board.GP10,board.GP9,  board.GP16, board.GP15,
          ),
    value_when_pressed=False
)


keymap = [
    ("A", [Keycode.A]),
    ("B", [Keycode.B]),
    ("C", [Keycode.C]),
    ("D", [Keycode.D]),
    ("E", [Keycode.E]),
    ("F", [Keycode.F]),
    ("G", [Keycode.G]),
    ("H", [Keycode.H]),
    ("I", [Keycode.I]),
    ("J", [Keycode.J]),
    ("Hi", "Hi"),
    ("Hey", "Hey"),
    ("Howdy", "Howdy"),
    ("Hola", "Hola"),
    ("Hiya", "Hiya"),
    ("Hei", "Hei")
]

keymap_mode_1 = [
    ("7", [Keycode.A]),
    ("8", [Keycode.B]),
    ("9", [Keycode.C]),
    ("Mode switch", [Keycode.D]),
    ("4", [Keycode.E]),
    ("5", [Keycode.F]),
    ("6", [Keycode.G]),
    ("Empty 8", [Keycode.H]),
    ("1", [Keycode.I]),
    ("2", [Keycode.J]),
    ("3", "Hi"),
    ("Empty 12", "Hey"),
    ("0", "Howdy"),
    ("Empty 14", "Hola"),
    ("Empty 15", "Hiya"),
    ("Empty 16", "Hei")
]

keymap_mode_2 = [
    ("Copy 1", [Keycode.A]),
    ("Copy 2", [Keycode.B]),
    ("Copy 3", [Keycode.C]),
    ("Mode switch", [Keycode.D]),
    ("Paste 1", [Keycode.E]),
    ("Paste 2", [Keycode.F]),
    ("Paste 3", [Keycode.G]),
    ("Clear", [Keycode.H]),
    ("Empty 9", [Keycode.I]),
    ("Up arrow", [Keycode.J]),
    ("Empty 11", "Hi"),
    ("Empty 12", "Hey"),
    ("Left Arrow", "Howdy"),
    ("Down Arrow", "Hola"),
    ("Right Arrow", "Hiya"),
    ("Empty 16", "Hei")
]

print("keymap:")
for key in keymap:
    print("\t", key[0])

while True:
    key_event = keys.events.get()
    if key_event:
        if key_event.pressed:
            print(keymap[key_event.key_number][0])
            pixel.fill(next(palette_iterator))
            sequence = keymap[key_event.key_number][1]
            for item in sequence:
                if isinstance(item, int):
                    if item >= 0:
                        kpd.press(item)
                    else:
                        kpd.release(-item)

                else:
                    keyboard_layout.write(item)
        else:
            # Release any still-pressed modifier keys
            for item in sequence:
                if isinstance(item, int) and item >= 0:
                    kpd.release(item)
            pixel.fill(mode_color[mode])
