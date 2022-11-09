import microbit
import lib
import time

lib.initCountdown(5)

print("\nmicro:bit connected\n")

while True:
    time.sleep(0.25)
    if microbit.button_a.was_pressed():  # type: ignore
        print("Button A pressed")
        time.sleep(0.5)
    if microbit.button_b.was_pressed():  # type: ignore
        print("Button B pressed")
        time.sleep(0.5)