import microbit
import lib
import pyautogui
import threading

lib.initCountdown(5)

print("\nmicro:bit connected\n")

threads = []

def lightC():
    pyautogui.click()

def rightC():
    pyautogui.rightClick()

def checkXAxis():
    x = microbit.accelerometer.get_x()  # type: ignore
    print("\nx is " + str(x) + "\n")

    if x >= 400:
        pyautogui.move(x/120,0)
    elif x <= -400:
        pyautogui.move(x/120,0)

def checkYAxis():
    y = microbit.accelerometer.get_y()  # type: ignore
    print("y is " + str(y) + "\n")

    if y >= 400:
        pyautogui.move(0,y/120)
    elif y <= -400:
        pyautogui.move(0,y/120)

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
