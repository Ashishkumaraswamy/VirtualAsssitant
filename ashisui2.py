from tkinter import*
from PIL import Image, ImageTk
import tkinter_tutorials as tt


def changesatus(text):
    statuslabel['text'] = text


def myfucntion():
    canvas.configure(scrollregion=canvas.bbox("all"))


def get_va_msg():
    msg = tt.first_1()
    if(msg['msg'] == ""):
        return
    show_msg(msg)
    root.update()
    changesatus("Processing..")
    root.update()
    msg = tt.run_alexa(msg['msg'])
    show_msg(msg)
    root.update()
    tt.talk(msg['msg'])
    changesatus("Listening..")
    root.update()


def show_msg(msg):
    print(msg)
    second_frame.width = 500
    second_frame.height = 600
    print(second_frame.winfo_height())
    print(second_frame.winfo_width())
    if msg['name'] == "You":
        msgframe = Frame(second_frame, bg='gray26')
        newmsg = Label(msgframe, text=msg['msg'], font=(
            "Georgia"), wraplength=200, padx=10, justify=LEFT)
        msgframe.pack(side=TOP, pady=10, fill=X, padx=20)
        newmsg.pack(side=RIGHT)
    else:
        msgframe = Frame(second_frame, bg='gray26')
        newmsg = Label(msgframe, text=msg['msg'], font=(
            "Georgia"), wraplength=200, padx=10, justify=LEFT)
        msgframe.pack(side=TOP, fill=X, pady=10, padx=10)
        newmsg.pack(side=LEFT)


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


root = Tk()
root.title("J.A.R.V.I.S")
root.iconbitmap('voice-assistant.ico')
frame1 = Frame(root, height=600, width=500,
               bg='gray26')
frame1.pack()
canvas = Canvas(frame1, height=600, width=500,
                bg='gray26', bd=2, relief=SUNKEN)
second_frame = Frame(canvas, height=600, width=500,
                     bg='gray26')
frame2 = Frame(root, height=150, width=500, bd=5)
frame2.pack(fill=X)
img = Image.open("keyboard.png")
img = img.resize((40, 40))
keyimg = ImageTk.PhotoImage(img)
keyboard = Button(frame2, image=keyimg, padx=2, pady=2,
                  width=40, height=40, relief=FLAT)
keyboard.grid(row=0, column=0, padx=20, pady=5)
statuslabel = Label(frame2, text="Listening...", height=2, width=30, padx=5, pady=5,
                    bg="gray26", fg="white", font=("Georgia", 12), relief=FLAT)
statuslabel.grid(row=0, column=2, padx=10, pady=5)
img = Image.open("settings.png")
img = img.resize((40, 40))
settingsimg = ImageTk.PhotoImage(img)
setting = Button(frame2, image=settingsimg, padx=2, pady=2,
                 width=40, height=40, relief=FLAT)
setting.grid(row=0, column=3, padx=20, pady=5)
scrollbar = Scrollbar(frame1, bg="white", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack()
canvas.create_window((0, 0), window=second_frame, anchor="nw")
second_frame.bind("<Configure>", lambda event,
                  canvas=canvas: onFrameConfigure(canvas))
second_frame.pack_propagate(0)
img = Image.open("avatar.jpg")
img = img.resize((50, 50))
avatarimg = ImageTk.PhotoImage(img)
avatarframe = Frame(second_frame, bg='gray26')
avatar = Label(avatarframe, image=avatarimg, anchor=E,
               height=50, width=50, padx=5, pady=5, bg="gray26", justify=RIGHT)
avatarframe.pack(side=TOP, pady=10, fill=X, padx=10)
avatar.pack(side=RIGHT, pady=10)
root.resizable(0, 0)
# msg = "Hello This is Ashish.How are you?adasdas sdsadsa sfasfa sfaafasfa "
# dictionary = {"msg": msg, "name": "Jarvis"}
# dictionary1 = {"msg": "Hello", "name": "Jarvis"}
# show_msg(dictionary)
# dictionary = {"msg": msg, "name": "You"}
# show_msg(dictionary)
# dictionary = {"msg": msg, "name": "You"}
# show_msg(dictionary)
# dictionary = {"msg": msg, "name": "Jarvis"}
# show_msg(dictionary)
# dictionary = {"msg": msg, "name": "Jarvis"}
# show_msg(dictionary1)
# dictionary = {"msg": msg, "name": "Jarvis"}
# show_msg(dictionary1)
# dictionary = {"msg": msg, "name": "You"}
# show_msg(dictionary)
# dictionary = {"msg": msg, "name": "You"}
# show_msg(dictionary)
# # self.window.after(1000, tt.first_run)
#         while(True):
#             self.window.after(2000, self.va)
#             self.window.update()
#         self.window.mainloop()
root.update()
msg = tt.first_run()
show_msg(msg)
root.update()
tt.talk(msg['msg'])
while(True):
    root.update()
    get_va_msg()
root.mainloop()
