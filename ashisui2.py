from tkinter import*
from PIL import Image, ImageTk
import tkinter_tutorials as tt

posy = 0.2


def myfucntion():
    canvas.configure(scrollregion=canvas.bbox("all"))


def show_msg(msg):
    global posy
    if msg['name'] == "You":
        newmsg = Label(second_frame, text=msg['msg'], font=(
            "Georgia", 12), wraplength=150, anchor="w")
        newmsg.place(relx=0.6, rely=posy, relwidth=0.32, relheight=0.1)
        posy += 0.12
    else:
        newmsg = Label(second_frame, text=msg['msg'], font=(
            "Georgia", 12), wraplength=150, anchor="w")
        newmsg.place(relx=0.1, rely=posy, relwidth=0.32, relheight=0.1)
        posy += 0.12


root = Tk()
root.title("J.A.R.V.I.S")
root.iconbitmap('voice-assistant.ico')

# root.geometry("600x800")
frame1 = Frame(root, height=600, width=500,
               bg='#11023E')
frame1.pack()
canvas = Canvas(frame1, height=600, width=500,
                bg='#11023E', bd=2, relief=SUNKEN)
canvas.pack()
frame2 = Frame(root, height=150, width=500, bd=5)
frame2.pack(fill=X)
img = Image.open("keyboard.png")
img = img.resize((40, 40))
keyimg = ImageTk.PhotoImage(img)
keyboard = Button(frame2, image=keyimg, padx=2, pady=2,
                  width=40, height=40, relief=FLAT)
keyboard.grid(row=0, column=0, padx=20, pady=5)
statuslabel = Label(frame2, text="Listening...", height=2, width=30, padx=5, pady=5,
                    bg="#11023E", fg="white", font=("Georgia", 12), relief=FLAT)
statuslabel.grid(row=0, column=2, padx=10, pady=5)
img = Image.open("settings.png")
img = img.resize((40, 40))
settingsimg = ImageTk.PhotoImage(img)
setting = Button(frame2, image=settingsimg, padx=2, pady=2,
                 width=40, height=40, relief=FLAT)
setting.grid(row=0, column=3, padx=20, pady=5)
scrollbar = Scrollbar(frame1, bg="white", command=canvas.yview)
scrollbar.place(relx=0.97, relheight=1)
canvas.config(yscrollcommand=scrollbar.set)

second_frame = Frame(canvas, height=600, width=500,
                     bg='#11023E')
second_frame.bind("<Configure>", myfucntion)
canvas.create_window((0, 0), window=second_frame, anchor="nw")
img = Image.open("avatar.jpg")
img = img.resize((50, 50))
avatarimg = ImageTk.PhotoImage(img)
avatar = Label(second_frame, image=avatarimg, anchor=E,
               height=50, width=50, padx=5, pady=5, bg="#11023E")
avatar.place(rely=0.04, relx=0.85)

msg = "Hello This is Ashish.How are you?"
dictionary = {"msg": msg, "name": "Jarvis"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "You"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "You"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "Jarvis"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "Jarvis"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "Jarvis"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "You"}
show_msg(dictionary)
dictionary = {"msg": msg, "name": "You"}
show_msg(dictionary)

root.mainloop()
