import microbit
import pyautogui
while True:
    if microbit.button_a.was_pressed():
        pyautogui.click()
