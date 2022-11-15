# Ignore all the # type: ignore
# They are for VSCode IntelliSense, so it doesn't say on each line that there's a error

# (I love PyLance)

#############################################################

import lib
import microbit
import time

print("\nmicro:bit connected\n")

#############################################################

def led(x, y, s):
    microbit.display.set_pixel(x, y, 9)  # type: ignore
    time.sleep(s/1000)
    microbit.display.set_pixel(x, y, 0)  # type: ignore
    time.sleep(s/1000)

#############################################################

xf = 4
yf = 0

num = (4, 2)

#############################################################

microbit.display.clear()  # type: ignore

lib.initCountdown(5)

while True:
    for x in num:
        if x == 4:
            n = 0
        else:
            n = 1
        for i in range(x):
            led(abs(min(-i, 0)) + n, n, 100)
        for i in range(x):
            led(4 - n, i + abs(~n) - ~n - 2 - n, 100)
        for i in range(x):
            led(4 - (i + abs(~n) - ~n - 2 - n), 4 - n, 100)
        for i in range(x):
            led(0 + n, 4 - (i + abs(~n) - ~n - 2 - n), 100)
        if n == 1: led(2, 2, 100)
