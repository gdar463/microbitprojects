# Credits to David Whale (whaleygeek)
# Github: https://github.com/whaleygeek
# Twitter: https://twitter.com/whaleygeek
# Website: http://www.thinkingbinaries.com/

# api.py  01/06/2017  D.J.Whale
#
# an API to a remote micro:bit
#
# TODO: for all pins: digital_write, digital_read
# TODO: for analog pins: analog_write, analog_read
# TODO: lots of other API methods that need implementing.

import time
import math

# NOTE: we have defined MicroBit as a class, so that it is possible later to
# have more than one micro:bit connected, perhaps with independent state
# such as the state of the REPL.

class MicroBit():
    def __init__(self, repl):
        self.repl                 = repl
        self.button_a.parent      = self  # type: ignore
        self.button_b.parent      = self  # type: ignore
        self.accelerometer.parent = self  # type: ignore
        self.display.parent       = self  # type: ignore
        self.pin0.parent          = self  # type: ignore
        self.pin1.parent          = self  # type: ignore
        self.pin2.parent          = self  # type: ignore
        self.radio.parent         = self  # type: ignore

    def cmd(self, command):
        ##print("send:%s" % command)
        self.repl.send_command(command)
        r = self.repl.wait_response()
        r = r.strip() # strip last NL from any print statement
        return r

    class TouchPin():
        def __init__(self, name):
            self.name = name

        def is_touched(self):
            r = self.parent.cmd("print(%s.is_touched())" % self.name)  # type: ignore
            r = eval(r)
            return r

    class Button():
        def __init__(self, name):
            self.name = name

        def was_pressed(self):
            r = self.parent.cmd("print(%s.was_pressed())" % self.name)  # type: ignore
            r = eval(r)
            return r

        def is_pressed(self):
            r = self.parent.cmd("print(%s.is_pressed())" % self.name)  # type: ignore
            r = eval(r)
            return r

    class Accelerometer():
        def __init__(self, name):
            self.name = name

        def get_x(self):
            r = self.parent.cmd("print(%s.get_x())" % self.name)  # type: ignore
            r = int(r)
            return r

        def get_y(self):
            r = self.parent.cmd("print(%s.get_y())" % self.name)  # type: ignore
            r = int(r)
            return r

        def get_z(self):
            r = self.parent.cmd("print(%s.get_z())" % self.name)  # type: ignore
            r = int(r)
            return r

        def get_values(self):
            r = self.parent.cmd("print(%s.get_values())" % self.name)  # type: ignore
            r = r[1:-1] # remove brackets
            r = r.split(",")
            r = (int(r[0]), int(r[1]), int(r[2]))
            return r
        
        def is_up(self):
            r = self.parent.cmd("print(%s.was_gesture('face up'))" % self.name)  # type: ignore
            r = eval(r)
            return r
        def is_down(self):
            r = self.parent.cmd("print(%s.was_gesture('face down'))" % self.name)  # type: ignore
            r = eval(r)
            return r

    class StandardImage():
        def __init__(self, name):
            self.name = name

    class Image():
        STD_IMAGE_NAMES = [
            "HEART", "HEART_SMALL", "HAPPY", "SMILE", "SAD", "CONFUSED", "ANGRY", "ASLEEP", "SURPRISED",
            "SILLY", "FABULOUS", "MEH", "YES", "NO", "TRIANGLE", "TRIANGLE_LEFT", "CHESSBOARD",
            "DIAMOND", "DIAMOND_SMALL", "SQUARE", "SQUARE_SMALL", "RABBIT", "COW",
            "MUSIC_CROTCHET", "MUSIC_QUAVER", "MUSIC_QUAVERS", "PITCHFORK", "XMAS", "PACMAN",
            "TARGET", "TSHIRT", "ROLLERSKATE", "DUCK", "HOUSE", "TORTOISE", "BUTTERFLY", "STICKFIGURE",
            "GHOST", "SWORD", "GIRAFFE", "SKULL", "UMBRELLA", "SNAKE",
            "CLOCK12","CLOCK11","CLOCK10","CLOCK9","CLOCK8","CLOCK7","CLOCK6","CLOCK5",
            "CLOCK4","CLOCK3","CLOCK2","CLOCK1",
            "ARROW_N", "ARROW_NE","ARROW_E","ARROW_SE","ARROW_S","ARROW_SW","ARROW_W","ARROW_NW"
        ]
        STD_IMAGES = []
        ##ALL_CLOCKS = []
        ##ALL_ARROWS = []

        def __init__(self, bitmap_str):
            self.bitmap_str = bitmap_str

        def __str__(self):
            return self.bitmap_str

    class Radio():
        def __init__(self, name):
            self.name = name

        def on(self):
            self.parent.cmd("import radio")  # type: ignore
            self.parent.cmd("%s.on()" % (self.name))  # type: ignore

        def config(self, **kwargs):
            self.parent.cmd("import radio")  # type: ignore
            kwargs_str = ', '.join('%s=%r' % x for x in kwargs.items())
            ##print(kwargs_str)
            self.parent.cmd("%s.config(%s)" % (self.name, kwargs_str))  # type: ignore

        def off(self):
            self.parent.cmd("%s.off()" % (self.name))  # type: ignore

        def send(self, message):
            self.parent.cmd("%s.send(\"%s\")" % (self.name, message))  # type: ignore

        def receive(self):
            #TODO: may need to add better handling of None somehow?
            return self.parent.cmd("print(%s.receive())" % (self.name))  # type: ignore

        def receive_bytes(self):
            data = self.parent.cmd("print(%s.receive_bytes())" % (self.name))  # type: ignore
            #TODO: may need to add better handling of None somehow?
            return data
        
        def reset(self):
            self.parent.cmd("%s.reset()" % (self.name))  # type: ignore

    class Display():
        def __init__(self, name):
            self.name = name

        def scroll(self, s):
            if not isinstance(s, str):
                raise RuntimeError("display.scroll needs a str")
            self.parent.cmd("%s.scroll(\"%s\")" % (self.name, s))  # type: ignore

        def show(self, v):
            if isinstance(v, MicroBit.StandardImage):
                self.parent.cmd("%s.show(Image.%s)" % (self.name, v.name))  # type: ignore

            elif isinstance(v, MicroBit.Image):
                s = v.__str__() # get bitmap
                self.parent.cmd("%s.show(Image(\"%s\"))" % (self.name, s))  # type: ignore

            elif isinstance(v, str):
                self.parent.cmd("%s.show(\"%s\")" % (self.name, v))  # type: ignore

            elif isinstance(v, int):
                if v >= 0 and v <= 99:
                    import font2x5
                    istr = font2x5.build_image_string(v)
                    self.parent.cmd("%s.show(Image(\"%s\"))" % (self.name, istr))  # type: ignore
                else:
                    v = str(v)
                    self.parent.cmd("%s.show(\"%s\")" % (self.name, v))  # type: ignore
            elif isinstance(v, list):
                #TODO: This is really an iterable.
                #but it is most likely a list of images such as ALL_CLOCKS
                raise RuntimeError("List parameters not yet implemented for Display.show()")

        def clear(self):
            self.parent.cmd("%s.clear()" % self.name)  # type: ignore

        def set_pixel(self, x, y, l):
            l = min(l, 9)
            l = max(l, 0)
            self.parent.cmd("display.set_pixel(" + str(x) + "," + str(y) + "," + str(l) + ")")  # type: ignore

    def sleep(self, ms):
        time.sleep(float(ms)/1000)

    def temperature(self):
        r = self.cmd("print(temperature())")
        r = int(r)
        return r

    def touch_logo_is_pressed(self):
        r = self.cmd("print(pin_logo.is_touched())")
        r = eval(r)
        return r

    button_a      = Button('button_a')
    button_b      = Button('button_b')
    accelerometer = Accelerometer("accelerometer")
    display       = Display("display")
    pin0          = TouchPin("pin0")
    pin1          = TouchPin("pin1")
    pin2          = TouchPin("pin2")
    radio         = Radio("radio")

    # Dynamically build attributes in Image for every standard image
    for image_name in Image.STD_IMAGE_NAMES:
        i = StandardImage(image_name)
        setattr(Image, image_name, i)
        Image.STD_IMAGES.append(i)

    # Dynamically build Image.ALL_CLOCKS now Image.CLOCK* is defined
    Image.ALL_CLOCKS = [  # type: ignore
        Image.CLOCK12, Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5,   # type: ignore
        Image.CLOCK6, Image.CLOCK7, Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11  # type: ignore
    ]

    # Dynamically build Image.ALL_ARROWS
    Image.ALL_ARROWS = [  # type: ignore
        Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE,  # type: ignore
        Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW  # type: ignore
    ]


# END
