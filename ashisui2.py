from tkinter import*
from PIL import Image, ImageTk
import tkinter_tutorials as tt
from threading import *
from tkinter import ttk
import datetime
import pywhatkit
import re
import time
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def changesatus(text):
    statuslabel['text'] = text


def sendwhatsappmsg(ph_no, phonewindow):
    phonewindow.destroy()
    show_msg(dict({'name': 'Jarvis', 'msg': "What is the message?"}))
    root.update()
    tt.talk("What is the message?")
    note_text = tt.first_1()
    show_msg(note_text)
    root.update()
    a = 1
    if(a == 59 and int(datetime.datetime.now().strftime("%S")) <= 40):
        a = 0
    tt.talk("Your message will be sent shortly to "+ph_no)
    show_msg(
        dict({'name': 'Jarvis', 'msg': "Your message will be sent shortly to "+ph_no}))
    root.update()
    pywhatkit.sendwhatmsg(f"+91{ph_no}", note_text['msg'], int(datetime.datetime.now(
    ).strftime("%H")), int(datetime.datetime.now().strftime("%M"))+a)

    get_va_msg()


def sendmail(ph_no, phonewindow):
    phonewindow.destroy()
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What is the subject?"}))
    root.update()
    tt.talk("What is the subject?")
    sub = tt.first_1()
    show_msg(sub)
    root.update()
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What is the message?"}))
    root.update()
    tt.talk("What is the message?")
    note_text = tt.first_1()
    show_msg(note_text)
    root.update()
    pywhatkit.send_mail("socialmediaatwork123@gmail.com",
                        "Qwerty123@", sub['msg'], note_text['msg'], ph_no)
    show_msg(
        dict({'name': 'Jarvis', 'msg': "Email sent successfully to "+ph_no}))
    root.update()
    tt.talk("Email sent successfully to "+ph_no)
    get_va_msg()


def validatephone(entry, errortext, phonewindow):
    phoneinput = entry.get()
    print(phoneinput)
    if(len(phoneinput) == 10 and phoneinput.isnumeric() == True):
        sendwhatsappmsg(phoneinput, phonewindow)
    else:
        entry.delete(0, END)
        errortext['text'] = "Enter a Valid Phone Number"
        errortext['bg'] = "red"


def validateemail(entry, errortext, phonewindow):
    phoneinput = entry.get()
    print(phoneinput)
    if(re.search(regex, phoneinput)):
        sendmail(phoneinput, phonewindow)
    else:
        entry.delete(0, END)
        errortext['text'] = "Enter a Valid Email Number"
        errortext['bg'] = "red"


def mail_window():
    phone_window = Toplevel(root)
    phone_window.geometry("500x220")
    phone_window.title("Email ADDRESS")
    title = Label(phone_window, text="Email ID",
                  bg="green", justify=CENTER, font=("Goergia"))
    title.pack(fill=X, side=TOP)
    title.config(height=2)
    phoneframe = Frame(phone_window, bg="white")
    phoneframe.pack(fill=X, side=TOP)
    phoneframe.config(height=100)
    phoneframe.pack_propagate(0)
    errortext = Label(phoneframe, text="", bg="white", font=("Georgia"))
    errortext.pack(fill=X)
    entrylabel = Label(phoneframe, text="Enter Email ID:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    entry = Entry(phoneframe, justify=LEFT, width=50)
    entry.pack(side=RIGHT, padx=30)
    submitframe = Frame(phone_window, bg="white")
    submitframe.pack(side=TOP, fill=X)
    submitbtn = Button(submitframe, text="Submit", height=3, width=7,
                       justify=CENTER, font=("Georgia"), bg="black", fg="white", relief=FLAT, command=lambda: validateemail(entry, errortext, phone_window))
    submitbtn.pack(pady=20)
    root.update()
    show_msg(dict({'name': "Jarvis", 'msg': "Enter the Email address"}))
    root.update()
    tt.talk("Enter the Email address")


def phone_window():
    phone_window = Toplevel(root)
    phone_window.geometry("500x220")
    phone_window.title("Phone Number")
    title = Label(phone_window, text="Whatsapp Number",
                  bg="green", justify=CENTER, font=("Goergia"))
    title.pack(fill=X, side=TOP)
    title.config(height=2)
    phoneframe = Frame(phone_window, bg="white")
    phoneframe.pack(fill=X, side=TOP)
    phoneframe.config(height=100)
    phoneframe.pack_propagate(0)
    errortext = Label(phoneframe, text="", bg="white", font=("Georgia"))
    errortext.pack(fill=X)
    entrylabel = Label(phoneframe, text="Enter Mobile Number:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    entry = Entry(phoneframe, justify=LEFT, width=50)
    entry.pack(side=RIGHT, padx=30)
    submitframe = Frame(phone_window, bg="white")
    submitframe.pack(side=TOP, fill=X)
    submitbtn = Button(submitframe, text="Submit", height=3, width=7,
                       justify=CENTER, font=("Georgia"), bg="black", fg="white", relief=FLAT, command=lambda: validatephone(entry, errortext, phone_window))
    submitbtn.pack(pady=20)
    root.update()
    show_msg(dict({'name': "Jarvis", 'msg': "Enter the Phone Number"}))
    root.update()
    tt.talk("Enter the Phone Number")


def delete_window():
    for widgets in frame1.winfo_children():
        widgets.destroy()
    root.update()


def create_window():
    # contentwindow = canvas.create_window((4, 4), window=second_frame,
    #                                      anchor="nw", width=500)
    # second_frame.bind("<Configure>", lambda event,
    #                   canvas=canvas: onFrameConfigure(canvas))
    # img = Image.open("avatar.jpg")
    # img = img.resize((50, 50))
    # avatarimg = ImageTk.PhotoImage(img)
    avatarframe = Frame(frame1, bg='gray26')
    avatar = Label(avatarframe, image=avatarimg, anchor=E,
                   height=50, width=50, padx=5, pady=5, bg="gray26", justify=RIGHT)
    avatarframe.pack(side=TOP, pady=10, fill=X, padx=10)
    avatar.pack(side=RIGHT, pady=10)
    root.update()


def get_va_msg():
    msg = tt.first_1()
    if(msg['msg'] == ""):
        get_va_msg()
    elif(msg['msg'] == "send a message in whatsapp"):
        phone_window()
    elif(msg['msg'] == "send a mail") or (msg['msg'] == "send a email"):
        mail_window()
    else:
        show_msg(msg)
        root.update()
        changesatus("Processing..")
        root.update()
        msg = tt.run_alexa(msg['msg'])
        show_msg(msg)
        root.update()
        tt.talk(msg['msg'])
        time.sleep(1.5)
        changesatus("Listening..")
        root.update()
        delete_window()
        create_window()
        get_va_msg()


def show_msg(msg):
    print(msg)
    if msg['name'] == "You":
        msgframe = Frame(frame1, bg='gray26')
        newmsg = Label(msgframe, text=msg['msg'], font=(
            "Georgia"), wraplength=200, padx=10, justify=LEFT)
        msgframe.pack(side=TOP, pady=10, fill=X, padx=20)
        newmsg.pack(side=RIGHT)
        # root.update()
    else:
        msgframe = Frame(frame1, bg='gray26')
        newmsg = Label(msgframe, text=msg['msg'], font=(
            "Georgia"), wraplength=200, padx=10, justify=LEFT)
        msgframe.pack(side=TOP, fill=X, pady=10, padx=10)
        newmsg.pack(side=LEFT)
        # root.update()


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


root = Tk()
root.configure(bg="gray26")
root.title("J.A.R.V.I.S")
root.iconbitmap('voice-assistant.ico')
frame1 = Frame(root, height=600, width=500,
               bg='gray26')
frame1.pack_propagate(0)
frame1.pack()
frame2 = Frame(root, height=150, width=500, bd=5)
frame2.pack(fill=BOTH, expand=1)
img = Image.open("keyboard.png")
img = img.resize((40, 40))
keyimg = ImageTk.PhotoImage(img)
keyboard = Button(frame2, image=keyimg, padx=2, pady=2,
                  width=40, height=40, relief=FLAT)
keyboard.grid(row=0, column=0, padx=20, pady=5)
statuslabel = Label(frame2, text="Listening...", height=2, width=30, padx=5, pady=5,
                    bg="gray26", fg="white", font=("Georgia"), relief=FLAT)
statuslabel.grid(row=0, column=2, padx=10, pady=5)
img = Image.open("vabutton.png")
img = img.resize((40, 40))
va_btn = ImageTk.PhotoImage(img)
mic = Button(frame2, image=va_btn, borderwidth=0,
             )
mic.grid(row=0, column=3, padx=20, pady=5)
# second_frame.pack_propagate(0)
img = Image.open("avatar.jpg")
img = img.resize((50, 50))
avatarimg = ImageTk.PhotoImage(img)
avatarframe = Frame(frame1, bg='gray26')
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
# root.update()
# root.update()
msg = tt.first_run()
show_msg(msg)
root.update()
tt.talk(msg['msg'])
get_va_msg()
root.mainloop()
