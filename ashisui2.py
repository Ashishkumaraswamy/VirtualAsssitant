from tkinter import*
from PIL import Image, ImageTk
import tkinter_tutorials as tt
from threading import *
from tkinter import ttk
import datetime
import pywhatkit
import re
import time
import pytz
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def postevent(titleentry, descentry, startentry, endentry, phone_window):
    event = {
        'summary': 'Google I/O 2015',
        'location': 'Coimbatore',
        'description': '',
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': "Asia/Kolkata",
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': "Asia/Kolkata",
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    title = titleentry.get()
    desc = descentry.get()
    start = startentry.get()
    end = endentry.get()
    phone_window.destroy()
    event['summary'] = title
    event['description'] = desc
    print(start)
    event['start']['dateTime'] = str(start)
    event['end']['dateTime'] = str(end)
    print(event)
    tt.create_event(event)
    tt.talk("Event created successfully and added to google calendar")
    delete_window()
    create_window()
    get_va_msg()


def changesatus(text):
    statuslabel['text'] = text


def checkdetailswindow(eventtitle, eventdescription, start, end):
    phone_window = Toplevel(root)
    phone_window.geometry("500x500")
    phone_window.title("GOOGLE Events")
    title = Label(phone_window, text="Google Events",
                  bg="green", justify=CENTER, font=("Goergia"))
    title.pack(fill=X, side=TOP)
    title.config(height=2)
    phoneframe = Frame(phone_window, bg="white")
    phoneframe.pack(fill=X, side=TOP)
    phoneframe.config(height=100)
    phoneframe.pack_propagate(0)
    errortext = Label(phoneframe, text="",
                      bg="white", font=("Georgia"))
    errortext.pack(fill=X)
    entrylabel = Label(phoneframe, text="Event Title:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    titleentry = Entry(phoneframe, justify=LEFT, width=50)
    titleentry.insert(0, eventtitle)
    titleentry.pack(side=RIGHT, padx=30)
    descframe = Frame(phone_window, bg="white")
    descframe.pack(fill=X, side=TOP)
    descframe.config(height=100)
    descframe.pack_propagate(0)
    entrylabel = Label(descframe, text="Event Description:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    descentry = Entry(descframe, justify=LEFT, width=50)
    descentry.insert(0, eventdescription)
    descentry.pack(side=RIGHT, padx=30)
    startframe = Frame(phone_window, bg="white")
    startframe.pack(fill=X, side=TOP)
    startframe.config(height=100)
    startframe.pack_propagate(0)
    entrylabel = Label(startframe, text="Start Time:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    startentry = Entry(startframe, justify=LEFT, width=50)
    startentry.insert(0, start)
    startentry.pack(side=RIGHT, padx=30)
    endframe = Frame(phone_window, bg="white")
    endframe.pack(fill=X, side=TOP)
    endframe.config(height=100)
    endframe.pack_propagate(0)
    entrylabel = Label(endframe, text="End Time:",
                       bg="white", font=("Georgia"))
    entrylabel.pack(side=LEFT, padx=20)
    endentry = Entry(endframe, justify=LEFT, width=50)
    endentry.insert(0, end)
    endentry.pack(side=RIGHT, padx=30)
    submitframe = Frame(phone_window, bg="white")
    submitframe.pack(side=TOP, fill=X)
    submitbtn = Button(submitframe, text="Submit", height=3, width=7,
                       justify=CENTER, font=("Georgia"), bg="black", fg="white", relief=FLAT, command=lambda: postevent(titleentry, descentry, startentry, endentry, phone_window))
    submitbtn.pack(pady=20)
    root.update()
    show_msg(dict({'name': "Jarvis", 'msg': "Verify the event details"}))
    root.update()
    tt.talk("Verify the event details")


def timdefromtext(start_time):
    if "p.m" in start_time['msg']:
        if ':' in start_time['msg']:
            try:
                index = start_time['msg'].find(":")
                hours = int(start_time['msg'][index-1:index])
                hours = hours+12
                minutes = int(start_time['msg'][index+1:index+3])
                starttime = str(hours)+":"+str(minutes)+":00"
                print(starttime)
            except ValueError as e:
                print("Enter proper date and time")
        else:
            try:
                index = start_time['msg'].find('p.m')
                hours = int(start_time['msg'][index-1:index])
                hours += 12
                starttime = str(hours)+":00:00"
            except ValueError as e:
                print("Enter proper date and time")
    else:
        if ':' in start_time['msg']:
            try:
                index = start_time['msg'].find(":")
                hours = int(start_time['msg'][index-1:index])
                minutes = int(start_time['msg'][index+1:index+3])
                starttime = str(hours)+":"+str(minutes)+":00"
                print(starttime)
            except ValueError as e:
                print("Enter proper date and time")
        else:
            index = start_time['msg'].find('a.m')
            hours = int(start_time['msg'][index-1:index])
            starttime = str(hours)+":00:00"
    return starttime


def createevent_google(date):
    try:
        date = date.strftime("%Y-%m-%d")
        print(type(date))
    except AttributeError as e:
        tt.talk(e)
        delete_window()
        create_window()
        get_va_msg()
    utc = pytz.UTC
    # checkdetailswindow(
    #     "jarvis testing", "jarvis testing", "5.00pm", "6.00pm")
    show_msg(dict({'name': 'Jarvis', 'msg': 'What is the event title sir?'}))
    root.update()
    tt.talk('What is the event title sir?')
    while (True):
        event_title = tt.first_1()
        if event_title['msg'] != "":
            break
    show_msg(event_title)
    root.update()
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'Would u like to add any description of the event?'}))
    root.update()
    tt.talk('Would u like to add any description of the event?')
    while (True):
        event_description = tt.first_1()
        if event_description['msg'] != "":
            break
    show_msg(event_description)
    root.update()
    if event_description['msg'] == "no":
        event_description['msg'] = ""
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'What is the event start time?'}))
    root.update()
    tt.talk('What is the event start time?')
    while (True):
        start_time = tt.first_1()
        if start_time['msg'] != "":
            starttime = timdefromtext(start_time)
            # starttime = datetime.datetime.strptime(
            #     starttime, '%H:%M:%S').time()
            starttime = str(date)+"T"+starttime
            # starttime = starttime.astimezone(utc)
            print(starttime)
            break
    show_msg(start_time)
    root.update()
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'What is the event end time?'}))
    root.update()
    tt.talk('What is the event end time?')
    while (True):
        end_time = tt.first_1()
        if end_time['msg'] != "":
            endtime = timdefromtext(end_time)
            # endtime = datetime.datetime.strptime(
            #     endtime, '%H:%M:%S').time()
            endtime = date+'T'+str(endtime)
            # endtime = endtime.astimezone(utc)
            print(endtime)
            break
    show_msg(end_time)
    root.update()
    checkdetailswindow(
        event_title['msg'], event_description['msg'], starttime, endtime)


def sendwhatsappmsg(ph_no, phonewindow):
    phonewindow.destroy()
    show_msg(dict({'name': 'You', 'msg': ph_no}))
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
    delete_window()
    create_window()
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
    delete_window()
    create_window()
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
        show_msg(msg)
        root.update()
        phone_window()
    elif(msg['msg'] == "send a mail") or (msg['msg'] == "send a email"):
        show_msg(msg)
        root.update()
        mail_window()
    elif "create an event" in msg['msg']:
        show_msg(msg)
        root.update()
        date = tt.get_date(msg['msg'])
        createevent_google(date)
    elif 'rest' in msg['msg'] or 'sleep' in msg['msg']:
        show_msg(msg)
        root.update()
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        show_msg(dict(
            {'name': "Jarvis", 'msg': "Okay Guys I will just take a nap, Call me whenever u need my help"}))
        root.update()
        tt.talk(reply)
        time.sleep(1)
        exit()
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
