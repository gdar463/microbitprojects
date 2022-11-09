keysDict = {
    "Q" : 0x10,
    "W" : 0x11,
    "E" : 0x12,
    "R" : 0x13,
    "T" : 0x14,
    "Y" : 0x15,
    "U" : 0x16,
    "I" : 0x17,
    "O" : 0x18,
    "P" : 0x19,
    "A" : 0x1E,
    "S" : 0x1F,
    "D" : 0x20,
    "F" : 0x21,
    "G" : 0x22,
    "H" : 0x23,
    "J" : 0x24,
    "K" : 0x25,
    "L" : 0x26,
    "Z" : 0x2C,
    "X" : 0x2D,
    "C" : 0x2E,
    "V" : 0x2F,
    "B" : 0x30,
    "N": 0x31,
    "M" : 0x32,

    "LEFT_ARROW" : 0xCB,
    "RIGHT_ARROW" : 0xCD,
    "UP_ARROW" : 0xC8,
    "DOWN_ARROW": 0xD0,
    "ESC" : 0x01,
    "ONE" : 0x02,
    "TWO" : 0x03,
    "THREE" : 0x04,
    "FOUR" : 0x05,
    "FIVE" : 0x06,
    "SIX" : 0x07,
    "SEVEN" : 0x08,
    "EIGHT" : 0x09,
    "NINE" : 0x0A,
    "ZERO" : 0x0B,
    "MINUS" : 0x0C,
    "EQUALS" : 0x0D,
    "BACKSPACE" : 0x0E,
    "APOSTROPHE" : 0x28,
    "SEMICOLON" : 0x27,
    "TAB" : 0x0F,
    "CAPSLOCK" : 0x3A,
    "ENTER" : 0x1C,
    "LEFT_CONTROL" : 0x1D,
    "LEFT_ALT" : 0x38,
    "LEFT_SHIFT" : 0x2A,
    "RIGHT_SHIFT" : 0x36,
    "TILDE" : 0x29,
    "PRINTSCREEN" : 0x37,
    "NUM_LOCK" : 0x45,
    "SPACE" : 0x39,
    "DELETE" : 0x53,
    "COMMA" : 0x33,
    "PERIOD" : 0x34,
    "BACKSLASH" : 0x35,
    "FORWARDSLASH" : 0x2B,
    "LEFT_BRACKET" : 0x1A,
    "RIGHT_BRACKET": 0x1B,

    "F1" : 0x3B,
    "F2" : 0x3C,
    "F3" : 0x3D,
    "F4" : 0x3E,
    "F5" : 0x3F,
    "F6" : 0x40,
    "F7" : 0x41,
    "F8" : 0x42,
    "F9" : 0x43,
    "F10" : 0x44,
    "F11" : 0x57,
    "F1" : 0x58,

    "NUMPAD_0" : 0x52,
    "NUMPAD_1" : 0x4F,
    "NUMPAD_2" : 0x50,
    "NUMPAD_3" : 0x51,
    "NUMPAD_4" : 0x4B,
    "NUMPAD_5" : 0x4C,
    "NUMPAD_6" : 0x4D,
    "NUMPAD_7" : 0x47,
    "NUMPAD_8" : 0x48,
    "NUMPAD_9" : 0x49,
    "NUMPAD_PLUS" : 0x4E,
    "NUMPAD_MINUS" : 0x4A,
    "NUMPAD_PERIOD" : 0x53,
    "NUMPAD_ENTER" : 0x9C,
    "NUMPAD_BACKSLASH" : 0xB5,

    "LEFT_MOUSE" : 0x100,
    "RIGHT_MOUSE" : 0x101,
    "MIDDLE_MOUSE" : 0x102,
    "MOUSE3" : 0x103,
    "MOUSE4" : 0x104,
    "MOUSE5" : 0x105,
    "MOUSE6" : 0x106,
    "MOUSE7" : 0x107,
    "MOUSE_WHEEL_UP" : 0x108,
    "MOUSE_WHEEL_DOWN" : 0x109
}

import microbit
import lib
import pyautogui
import keys
import threading

lib.initCountdown(5)

print("\nmicro:bit connected\n")

threads = []
pyautogui.FAILSAFE = True
aTouch = input("What key do you want to press when using A and the gold logo? (it'll be pressed only for a bit, so not held down)\n> ").upper

def right():
    keys.HoldAndReleaseKey(0x20, 0.1)

def left():
    keys.HoldAndReleaseKey(0x1E, 0.1)

def up():
    keys.HoldAndReleaseKey(0x11, 0.1)

def down():
    keys.HoldAndReleaseKey(0x1F, 0.1)

def lightC():
    pyautogui.click()

def rightC():
    pyautogui.rightClick()

def aTouchFn():
    keyATouchIdx = [i for i, item in enumerate(keysDict.keys()) if item == aTouch]
    keyATouch = list(keysDict.values())[keyATouchIdx[0]]
    keys.HoldAndReleaseKey(keyATouch, 0.02)

def esc():
    keys.HoldAndReleaseKey(0x01, 0.02)

def checkXAxis():
    x = microbit.accelerometer.get_x()  # type: ignore
    print("\nx is " + str(x) + "\n")

    if x >= 350:
        if microbit.touch_logo_is_pressed():  # type: ignore
            pyautogui.move(x/120,0)
        else:
            print("right")
            threads.append(threading.Thread(target=right))
    elif x <= -350:
        if microbit.touch_logo_is_pressed():  # type: ignore
            pyautogui.move(x/120,0)
        else:
            print("left")
            threads.append(threading.Thread(target=left))

def checkYAxis():
    y = microbit.accelerometer.get_y()  # type: ignore
    print("y is " + str(y) + "\n")

    if y >= 350:
        if microbit.touch_logo_is_pressed():  # type: ignore
            pyautogui.move(0,y/120)
        else:
            print("down")
            threads.append(threading.Thread(target=down))
    elif y <= -350:
        if microbit.touch_logo_is_pressed():  # type: ignore
            pyautogui.move(0,y/120)
        else:
            print("up")
            threads.append(threading.Thread(target=up))

def checkButtons():
    if microbit.button_a.was_pressed():    # type: ignore
        if microbit.touch_logo_is_pressed():  # type: ignore
            threads.append(threading.Thread(target=aTouchFn))
        else:
            print("leftClick")
            threads.append(threading.Thread(target=lightC))
            # pyautogui.press("l")
    if microbit.button_b.was_pressed():    # type: ignore
        if microbit.touch_logo_is_pressed():  # type: ignore
            threads.append(threading.Thread(target=esc))
        else:
            print("rightClick")
            threads.append(threading.Thread(target=rightC))
            # pyautogui.press("r")

while True:
    checkXAxis()
    checkYAxis()
    checkButtons()

    print(threads)

    for x in threads:
        x.start()

    print(threads)

    for x in threads:
        x.join()

    print(threads)

    for i in range(len(threads)):
        threads.pop(0)

    print(threads)
