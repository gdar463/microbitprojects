import microbit
import lib
import time
import pyautogui

lib.initCountdown(5)

print("\nmicro:bit connected\n")

while True:
    time.sleep(0.25)
    if microbit.button_a.was_pressed():  # type: ignore
        print("Left")
        pyautogui.leftClick()
    if microbit.button_b.was_pressed():  # type: ignore
        print("Right")
        pyautogui.rightClick()