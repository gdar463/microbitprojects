# Micro:Bit Projects

My Micro:Bit projects

## Installing

Install git if you haven't already, then execute in a terminal:  
```
git clone https://github.com/gdar463/microbitprojects.git
```
Flash on the Micro:Bit the bitio.hex file.  
If you haven't before, install python with pip, add to path python (with installer or manually).  
In a terminal execute:
```
pip install -r requirments.txt
```
If it doesn't work use:  
```
py -m pip install -r requirments.txt
```

## What's in this mess

At the moment there's:  
- KeyOuse, that uses the accelormeter as a way to press keys and move the cursor.
    - There are two versions:
        - norKeyOuse.py, for normal use case so only mouse and 2 keys
        - gamKeyOuse.py, meant for games so WASD, mouse and 2 keys

## Credits

[DougDoug](https://youtube.com/user/Gloudas) for the keyboard handling

[whaleygeek](https://github.com/whaleygeek/bitio) for bitio, essential for Micro:Bit