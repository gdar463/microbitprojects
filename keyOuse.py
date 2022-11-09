import microbit
import lib
import pyautogui
import keys
import threading
import serial

lib.initCountdown(5)

print("\nmicro:bit connected\n")

threads = []
pyautogui.FAILSAFE = True
# serialString = ""
# serialPort = serial.Serial(port = "COM3", baudrate=115200,bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE)

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

def e():
    keys.HoldAndReleaseKey(0x12, 0.02)

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
            threads.append(threading.Thread(target=e))
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