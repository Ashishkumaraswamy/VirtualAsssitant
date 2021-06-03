from tkinter import*
from PIL import Image, ImageTk
import tkinter_tutorials as tt

posy = 0.2


def changesatus(text):
    statuslabel['text'] = text


def myfucntion():
    canvas.configure(scrollregion=canvas.bbox("all"))


def get_va_msg():
    print('Here')
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
    print("Here")
    global posy
    print(msg)
    length = len(msg['msg'])
    width = int(length/15)
    if width > 0:
        width_change = 0
    else:
        width_change = length % 15
    height = int(length/20)
    if msg['name'] == "You":
        print("Inside Hre")
        newmsg = Label(second_frame, text=msg['msg'], font=(
            "Georgia", 12), wraplength=150, borderwidth=2)
        newmsg.corner_radius = 5
        newmsg.border_width = 2
        newmsg.place(relx=0.6+width_change*0.005, rely=posy, relwidth=0.33-width_change*0.005,
                     relheight=0.025+(height+1)*0.032, anchor="w")
        posy += 0.04+(height+1)*0.032
    else:
        newmsg = Label(second_frame, text=msg['msg'], font=(
            "Georgia", 12), wraplength=150, borderwidth=2)
        newmsg.corner_radius = 5
        newmsg.border_width = 2
        newmsg.place(relx=0.04, rely=posy, relwidth=0.33-width_change*0.0005,
                     relheight=0.025+(height+1)*0.032, anchor="w")
        posy += 0.04+(height+1)*0.032


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


root = Tk()
root.title("J.A.R.V.I.S")
root.iconbitmap('voice-assistant.ico')

# root.geometry("600x800")
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
scrollbar.place(relx=0.97, relheight=1)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack()
canvas.create_window((0, 0), window=second_frame, anchor="nw")
second_frame.bind("<Configure>", lambda event,
                  canvas=canvas: onFrameConfigure(canvas))
img = Image.open("avatar.jpg")
img = img.resize((50, 50))
avatarimg = ImageTk.PhotoImage(img)
avatar = Label(second_frame, image=avatarimg, anchor=E,
               height=50, width=50, padx=5, pady=5, bg="gray26")
avatar.place(rely=0.04, relx=0.85)

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
