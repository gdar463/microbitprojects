from .microbit.__init__ import *
import lib
import pyautogui
import keys
import threading
import time

lib.initCountdown(5)

print("\nmicro:bit connected\n")

threads = []
pyautogui.FAILSAFE = True

def checkXAxis():
    time.sleep(0.5)
    x = microbit.accelerometer.get_x()
    print("\nx is " + str(x) + "\n")

    if x >= 350:
        print("right")
        keys.HoldAndReleaseKey(0x20, 0.3)
    elif x <= -350:
        print("left")
        keys.HoldAndReleaseKey(0x1E, 0.3)

def checkYAxis():
    time.sleep(0.5)
    y = microbit.accelerometer.get_y()
    if y >= 350:
        print("down")
        keys.HoldAndReleaseKey(0x1F, 0.3)
    elif y <= -350:
        print("up")
        keys.HoldAndReleaseKey(0x11, 0.3)

def checkButtons():
    time.sleep(0.5)
    if microbit.button_a.was_pressed():  
        print("leftClick")
        pyautogui.leftClick()
        # pyautogui.press("l")
    if microbit.button_b.was_pressed():  
        print("rightClick")
        pyautogui.rightClick()
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

    # for t in threads:
    #     t.join()

    checkXAxis()
    checkYAxis()
    checkButtons()
    time.sleep(0.5)