from ahk import AHK
import time

ahk = AHK()

def forward():
    ahk.key_down('w')
    time.sleep(0.5)
    ahk.key_up('w')

def backward():
    ahk.key_down('s')
    time.sleep(0.5)
    ahk.key_up('s')

def left():
    x, y = ahk.mouse_position
    ahk.click(x=x, y=y)

def right():
    x, y = ahk.mouse_position
    ahk.right_click(x=x, y=y)

def inv():
    ahk.key_press('e')

def note(note):
    if note == "C":
        backward()
    elif note == "D":
        forward()
    elif note == "E":
        left()
    elif note == "F":
        right()
    elif note == "G":
        inv()
    else:
        print(f"Invalid note: {note}")