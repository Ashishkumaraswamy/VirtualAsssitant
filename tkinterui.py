from tkinter import *
from PIL import ImageTk, Image
size = 10
animationOn = False
(width, height) = (400, 400)


def simpleAnimation():
    global label, height, width
    im = Image.new("RGB", (400, 400), (255, 255, 255))
    root = Tkinter.Tk()
    photo = ImageTk.PhotoImage(im)
    label = Tkinter.Label(root, image=photo)
    label.image = photo
    label.pack()
    buttonHolder = Tkinter.Frame(root)
    start = Tkinter.Button(buttonHolder, text="Start", command=startAnimation)
    stop = Tkinter.Button(buttonHolder, text="Stop", command=stopAnimation)
    buttonHolder.pack()
    start.pack(side="left")
    stop.pack(side="right")
    animate()
    root.mainloop()


def startAnimation():
    global animationOn
    animationOn = True
    animate()


def stopAnimation():
    global animationOn
    animationOn = False


def animate():
    global size, label, width, height
    newIm = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(newIm)
    (cX, cY) = (width/2, height/2)
    draw.ellipse([cX-size/2, cY-size/2, cX+size/2, cY+size/2], (0, 0, 0))
    photo = ImageTk.PhotoImage(newIm)
    label.configure(image=photo)
    label.image = photo
    # This next line is what controls the animation.  It tells python to
    # call the animate function again after 100 milliseconds.  These are
    # the first two parameters (delay time, and then function to call)

    if animationOn:
        size += 10
        label.after(100, animate)


simpleAnimation()
