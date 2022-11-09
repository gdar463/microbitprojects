import microbit
import lib
import pyautogui
import keys
import threading
import time

lib.initCountdown(5)

print("\nmicro:bit connected\n")

threads = []
pyautogui.FAILSAFE = True

def right():
    keys.HoldAndReleaseKey(0x20, 0.5)

def left():
    keys.HoldAndReleaseKey(0x1E, 0.5)

def up():
    keys.HoldAndReleaseKey(0x11, 0.5)

def down():
    keys.HoldAndReleaseKey(0x1F, 0.5)

def lightC():
    pyautogui.click()

def rightC():
    pyautogui.rightClick()

def checkXAxis():
    x = microbit.accelerometer.get_x()  # type: ignore
    print("\nx is " + str(x) + "\n")

    if x >= 350:
        print("right")
        threads.append(threading.Thread(target=right))
    elif x <= -350:
        print("left")
        threads.append(threading.Thread(target=left))

def checkYAxis():
    y = microbit.accelerometer.get_y()  # type: ignore
    print("y is " + str(y) + "\n")

    if y >= 350:
        print("down")
        threads.append(threading.Thread(target=down))
    elif y <= -350:
        print("up")
        threads.append(threading.Thread(target=up))

def checkButtons():
    if microbit.button_a.was_pressed():    # type: ignore
        print("leftClick")
        threads.append(threading.Thread(target=lightC))
        # pyautogui.press("l")
    if microbit.button_b.was_pressed():    # type: ignore
        print("rightClick")
        threads.append(threading.Thread(target=rightC))
        # pyautogui.press("r")

while True:
    # if len(threads) == 3:
    #     pass
    # else:
    #     for i in range(3):
    #         if i == 0:
    #             t = threading.Thread(target=checkXAxis)
    #         elif i == 1:
    #             t = threading.Thread(target=checkYAxis)
    #         elif i == 2:
    #             t = threading.Thread(target=checkButtons)
    #         threads.append(t)  # type: ignore
    #         t.start()   # type: ignore

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