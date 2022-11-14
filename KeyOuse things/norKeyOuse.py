# This is intended for normal use case so only mouse and 2 keys

# Ignore all the # type: ignore
# They are for VSCode IntelliSense, so it doesn't say on each line that there's a error

# (I love PyLance)

#############################################################

import microbit
import lib
import pyautogui
import keys
import threading

print("\nmicro:bit connected\n")

#############################################################

# Various Variables
keysDict = {}
threads = []
pyautogui.FAILSAFE = True
version = int("".join(filter(str.isdigit, str(input("What version is your microbit? (1 or 2) (If 1 it removes the gold logo functionality)\n> "))))[:1])
if version != 1:
    aTouch = str(input("\nWhat key do you want to press when using A and the gold logo? (it'll be pressed only twenty milliseconds, so not held down) (for the key check keysdict.txt and type here the key in the first column you want)\n> "))
    bTouch = str(input("\nWhat key do you want to press when using B and the gold logo? (it'll be pressed only twenty milliseconds, so not held down) (for the key check keysdict.txt and type here the key in the first column you want)\n> "))

# How to reduce a 101-lines dictionary in a 9-lines mess
f = open("keysdict.txt","r")
keysDictFile = f.read()
keysDictLines = keysDictFile.splitlines()
keysDictDouble = str(keysDictLines).replace("[","").replace("]","").replace(" ","").replace("(","").replace(")","").replace("'","").split(":")
keysDictSingle = str(keysDictDouble).replace("[","").replace("]","").replace(" ","").replace("(","").replace(")","").replace("'","").split(",")
for x in range(len(keysDictLines)):
    keysDict.update({keysDictSingle[0]: keysDictSingle[1]})
    keysDictSingle.pop(1)
    keysDictSingle.pop(0)
f.close()

# It's the Final Coutdown
lib.initCountdown(5)  # type: ignore

#############################################################

# Keys Function
def lightC():
    pyautogui.click()

def rightC():
    pyautogui.rightClick()

def aTouchFn():
    keyATouch = [x for x in list(keysDict.keys()) if x == aTouch.upper()]
    keyHexATouchIdx = list(keysDict.keys()).index(keyATouch[0])
    keyHexATouch = list(keysDict.values())[keyHexATouchIdx]
    keys.HoldAndReleaseKey(keyHexATouch, 0.02)

def bTouchFn():
    keyBTouch = [x for x in list(keysDict.keys()) if x == bTouch.upper()]
    keyHexBTouchIdx = list(keysDict.keys()).index(keyBTouch[0])
    keyHexBTouch = list(keysDict.values())[keyHexBTouchIdx]
    keys.HoldAndReleaseKey(keyHexBTouch, 0.02)

#############################################################

# format for checking:
# if microbit.touch_logo_is_pressed(): # Checks if touch Logo is pressed                        type: ignore
#   print("<what happened>")
#   <Code if logo touched>
# else:
#   print("<what happened>")
#   <Normal Code>

# format for threads:
# threads.append(threading.Thread(target = <function>))

# Check Micro:Bit
def checkXAxis():
    x = microbit.accelerometer.get_x()  # type: ignore
    if x >= 350:
        print("right")
        pyautogui.move(x/120,0)
    elif x <= -350:
        print("left")
        pyautogui.move(x/120,0)

def checkYAxis():
    y = microbit.accelerometer.get_y()  # type: ignore
    if y >= 350:
        print("down")
        pyautogui.move(0,y/120)
    elif y <= -350:
        print("up")
        pyautogui.move(0,y/120)

def checkButtons():
    # Button A
    if microbit.button_a.was_pressed():    # type: ignore
        if not version == 1 and microbit.touch_logo_is_pressed():  # type: ignore
            print("aTouch")
            threads.append(threading.Thread(target = aTouchFn))
        else:
            print("leftClick")
            threads.append(threading.Thread(target = lightC))
    # Button B
    if microbit.button_b.was_pressed():    # type: ignore
        if not version == 1 and microbit.touch_logo_is_pressed():  # type: ignore
            print("bTouch")
            threads.append(threading.Thread(target = bTouchFn))
        else:
            print("rightClick")
            threads.append(threading.Thread(target = rightC))

#############################################################

# Real part
while True:
    checkXAxis()
    checkYAxis()
    checkButtons()

    # Threads Handling
    for x in threads:
        x.start()

    for x in threads:
        x.join()

    for i in range(len(threads)):
        threads.pop(0)
