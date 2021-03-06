"""

                    _/                                                    _/
         _/_/_/          _/_/_/    _/_/        _/_/_/      _/_/_/    _/_/_/
        _/    _/  _/  _/        _/    _/      _/    _/  _/    _/  _/    _/
       _/    _/  _/  _/        _/    _/      _/    _/  _/    _/  _/    _/
      _/_/_/    _/    _/_/_/    _/_/        _/_/_/      _/_/_/    _/_/_/
     _/                                    _/
    _/                                    _/

    Code loosely adapted from the following sources:
    MACROPAD Hotkey (https://learn.adafruit.com/macropad-hotkeys/project-code)
    Pico Four Keypad  (https://learn.adafruit.com/pico-four-key-macropad/code-the-four-keypad)
    https://github.com/jpconstantineau/pykey/blob/main/examples/Raspberry_Pi_Pico_4x4_Macropad_v2/code.py

"""
import board
import keypad
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_itertools.adafruit_itertools import cycle

def swap(mode):
    return 1-mode


def quine():
    print(open(__file__).read())

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
    ("7", [Keycode.KEYPAD_SEVEN]),
    ("8", [Keycode.KEYPAD_EIGHT]),
    ("9", [Keycode.KEYPAD_NINE]),
    ("Numlock", [Keycode.KEYPAD_NUMLOCK]),
    ("4", [Keycode.KEYPAD_FOUR]),
    ("5", [Keycode.KEYPAD_FIVE]),
    ("6", [Keycode.KEYPAD_SIX]),
    ("Delete", [Keycode.BACKSPACE]),
    ("1", [Keycode.KEYPAD_ONE]),
    ("2", [Keycode.KEYPAD_TWO]),
    ("3", [Keycode.KEYPAD_THREE]),
    ("Enter", [Keycode.KEYPAD_ENTER]),
    ("0", [Keycode.KEYPAD_ZERO]),
    ("Copy", [Keycode.LEFT_CONTROL, Keycode.C]),
    ("Paste", [Keycode.LEFT_CONTROL, Keycode.V]),
    ("Save Quit", [":wq!"])
]

keymap_mode_1 = [
    ("7", [kpd.send, [Keycode.KEYPAD_SEVEN]]),
    ("8", [kpd.send, [Keycode.KEYPAD_EIGHT]]),
    ("9", [kpd.send, [Keycode.KEYPAD_NINE]]),
    ("Swap", [swap]),
    ("4", [kpd.send, [Keycode.KEYPAD_FOUR]]),
    ("5", [kpd.send, [Keycode.KEYPAD_FIVE]]),
    ("6", [kpd.send, [Keycode.KEYPAD_SIX]]),
    ("Backspace", [kpd.send, [Keycode.BACKSPACE]]),
    ("1", [kpd.send, [Keycode.KEYPAD_ONE]]),
    ("2", [kpd.send, [Keycode.KEYPAD_TWO]]),
    ("3", [kpd.send, [Keycode.KEYPAD_THREE]]),
    ("Enter", [kpd.send, [Keycode.KEYPAD_ENTER]]),
    ("0", [kpd.send, [Keycode.KEYPAD_ZERO]]),
    ("Select All", [kpd.send, [Keycode.LEFT_CONTROL, Keycode.A]]),
    ("Copy", [kpd.send, [Keycode.LEFT_CONTROL, Keycode.C]]),
    ("Paste", [kpd.send, [Keycode.LEFT_CONTROL, Keycode.V]])
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
