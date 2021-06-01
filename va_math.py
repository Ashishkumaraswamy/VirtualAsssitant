from tkinter import *
from PIL import ImageTk, Image
import tkinter_tutorials as ob

def vabutton():
    label['text'] = "listening..."
    label['text'] = ob.run_alexa()

HEIGHT = 550
WIDTH = 450
root = Tk()
root.title("J.A.R.V.I.S")
root.geometry("600x600")
root.iconbitmap('voice-assistant.ico')

# bg_image = Image.open("jarvis.jpg")
# bg_image = bg_image.resize((700, 450))
# bg_image = ImageTk.PhotoImage(bg_image)
# bg_label = Label(image=bg_image)
# bg_label.place(relheight=1, relwidth=1)




va_btn = PhotoImage(file='vabutton.png')
button = Button(root,image=va_btn,borderwidth=0,command=vabutton)
button.pack(padx=10)

frame_output = Frame(root, bg="#99b3e6", bd=3)
frame_output.place(relx=0.05, rely=0.5, relheight=0.35,
                   relwidth=0.90)

label = Label(frame_output, bg="grey", fg='white', font=(
    'courier', 16), anchor='nw', justify='left', bd=4)
label.place(relheight=1, relwidth=1)


root.mainloop()

