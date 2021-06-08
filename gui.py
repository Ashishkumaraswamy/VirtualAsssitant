from __future__ import print_function
from copy import error
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import subprocess
import os
import pyscreenshot
import pytz
import webbrowser
import psutil
import pyautogui
from PyDictionary import PyDictionary
from calculator.simple import SimpleCalculator
from tkinter import*
from PIL import Image, ImageTk
import re
import time



regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
dictionary = PyDictionary()


def authorize_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    returnlist = ""
    if not events:
        print('No upcoming events found.')
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        find = start.find('T')
        start = start[find+1:find+6]+start[find+15:]+" "
        print(start, event['summary'])
        returnlist += start
        returnlist += event['summary']
        returnlist += "\n"
    return returnlist


def create_event(event):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(event)
    except:
        print(event)
        print("Enter a proper date. Failed to create event. Enter a proper date.")
        talk("Enter a proper date. Failed to create event. Enter a proper date.")
    print('Event created:', event.get('htmlLink'))


def get_date(text):
    try:
        text = text.lower()
        today = datetime.date.today()

        if text.count("today") > 0:
            return today
        elif "tomorrow" in text:
            day = today.day+1
            month = today.month
            year = today.year
            return datetime.date(month=month, day=day, year=year)

        day = -1
        day_of_week = -1
        month = -1
        year = today.year

        for word in text.split():
            if word in MONTHS:
                month = MONTHS.index(word) + 1
            elif word in DAYS:
                day_of_week = DAYS.index(word)
            elif word.isdigit():
                day = int(word)
            else:
                for ext in DAY_EXTENTIONS:
                    found = word.find(ext)
                    if found > 0:
                        try:
                            day = int(word[:found])
                        except ValueError as e:
                            pass

        if month < today.month and month != -1:
            year = year+1

        if month == -1 and day != -1:
            if day < today.day:
                month = today.month + 1
            else:
                month = today.month

        if month == -1 and day == -1 and day_of_week != -1:
            current_day_of_week = today.weekday()
            dif = day_of_week - current_day_of_week

            if dif < 0:
                dif += 7
                if text.count("next") >= 1:
                    dif += 7

            return today + datetime.timedelta(dif)

        if day != -1:
            return datetime.date(month=month, day=day, year=year)
    except ValueError as e:
        print(e)
        talk(e)


def first_run():
    welcome_msg = "HI Project Members This is Jarvis here!!.Current time is {}. An exciting day awaits before you .!!".format(
        datetime.datetime.now().strftime('%I:%M %p'))
    engine.runAndWait()
    return dict({'name': 'Jarvis', 'msg': welcome_msg})


def talk(text):
    engine.say(text)
    engine.runAndWait()


def first_1():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(
                voice, key=None, language='en-in', show_all=True)
            print(command)
            if command != []:
                command = command['alternative'][0]['transcript']
                command = command.lower()
            else:
                command = ""
    except:
        pass
    return dict({"name": "You", "msg": command})


def run_alexa(command):
    if command == "No command recieved":
        reply = "No command recieved"
    elif 'hello' in command or 'hi' in command:
        reply = "Hello sir!!"
    elif 'how are you' in command:
        reply = "I am fine, Thank you"
        reply += ",How are you, Sir?"
    elif 'search' in command:
        inp = command.replace('search', '')
        reply = 'searching ' + inp
        pywhatkit.search(inp)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        reply = 'Current time is ' + time
    elif 'tell me about' in command:
        person = command.replace('tell me about', '')
        reply = wikipedia.summary(person, 1)
    elif 'joke' in command:
        reply = pyjokes.get_joke()
    elif 'play' in command:
        song = command.replace('play', '')
        reply = 'playing ' + song
        pywhatkit.playonyt(song)

    elif 'battery percentage' in command or 'battery info' in command or 'battery information' in command:
        battery_data = psutil.sensors_battery()
        if battery_data.power_plugged:
            strg = ' charging '
        else:
            strg = ' not charging '
        reply = "Your system is currently "+strg+"and it is " + \
            format(battery_data.percent)+" percent."

    elif 'take screenshot' in command:
        talk("Taking screenshot")
        image = pyscreenshot.grab()
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-")+"-screenshot.png"
        image.save(file_name)
        image.show()
        reply = "Took the screenshot"
    elif 'tell me the events' in command:
        service = authorize_google()
        date = get_date(command)
        reply = get_events(date, service)
    elif 'open spotify' in command:
        subprocess.Popen(['spotify.exe'])
        reply = "Opened Spotify application"

    elif 'calculate' in command:
        inp = command.replace('calculate', '')
        if 'divide' in command:
            inp = inp.replace('divide', '/')
        if 'by' in command:
            inp = inp.replace('by', '/')
        c = SimpleCalculator()
        c.run(inp)
        d = c.lcd
        reply = "Answer is :" + str(d)

    elif 'open myanimelist' in command or 'open stackoverflow' in command or 'open youtube' in command or 'open github' in command or 'open nucleus' in command or 'open moodle' in command:
        inp = command.replace('open', '')
        inp = inp.replace(' ', '')
        talk("Opening "+inp+" Sir!!")
        b = webbrowser.get()

        if(inp == "myanimelist"):
            b.open("https://myanimelist.net")
        elif (inp == "stackoverflow"):
            b.open("https://stackoverflow.com")
        elif (inp == "youtube"):
            b.open("https://www.youtube.com")
        elif (inp == "github"):
            b.open("https://github.com")
        elif (inp == "nucleus"):
            b.open("https://nucleus.amcspsgtech.in")
        elif (inp == "moodle"):
            b.open("https://moodle.amcspsgtech.in")
        reply = "Opened "+inp+" in your web browser"

    # elif 'open spotify' in command:
    #     talk("Opening Spotify Sir!!")
    #     subprocess.Popen(['spotify.exe'])
    #     #subprocess.run(['spotify.exe'],input="dive back in time",)
    #     # b=webbrowser.get()
    #     # b.open("https://open.spotify.com")
    #     reply = "Opened Spotify application"
    elif "close camera" in command:
        try:
            d = subprocess.run('Taskkill /IM WindowsCamera.exe /F',
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            pass
        reply = "Camera application is closed"
    elif "camera" in command or "take a photo" in command:
        subprocess.run('start microsoft.windows.camera:', shell=True)
        reply = "Opened Camera application"
    elif "volume up" in command or "increase volume" in command or "increase sound" in command or "increase the volume" in command or "increase the sound" in command:
        pyautogui.press("volumeup")
        reply = "Increased the volume sir!!"
    elif "volume down" in command or "decrease volume" in command or "decrease sound" in command or "decrease the volume" in command or "decrease the sound" in command:
        pyautogui.press("volumedown")
        reply = "decreased the volume sir!!"
    elif "mute" in command:
        pyautogui.press("volumemute")
        if "unmute" in command:
            reply = "system unmute sir!!"
        else:
            reply = "system mute sir!!"

    elif "close chrome" in command or "close webbrowser" in command or "close web browser" in command:
        subprocess.call("taskkill /IM chrome.exe")
        reply = "chrome closed sir!!"
    elif "where is" in command or "locate" in command:

        if "where is" in command:
            query = command.replace("where is", "")
        else:
            query = command.replace("locate", "")
        location = query
        webbrowser.open("https://www.google.com/maps/place/" + location + "")
        reply = "User asked to Locate" + location

    elif "what's your name" in command or "what is your name" in command:
        reply = "My name is Jarvis a virtual assistant!!"

    elif 'exit' in command:
        talk("Thanks for giving me your time see you soon")
        exit()

    elif "who made you" in command or "who created you" in command or "who is your god" in command:
        reply = "I have been created by 3 idiots Ashish mathan sai shyam!!."

    elif "will you be my gf" in command or "will you be my bf" in command or "will you be my girl friend" in command or "will you be my girlfriend" in command:
        reply = "I'm not sure about, may be you should give me some time"
    elif "i love you" in command:
        reply = "It's hard to understand"

    elif 'find the meaning of' in command:
        inp = command.replace('find the meaning of', '')
        inp = inp.replace(' ', '')
        out = dictionary.meaning(inp)
        list = [(k, v) for k, v in out.items()]
        out = ""
        for x in list:
            out += x[0] + " : "+x[1][0]+"\n"
        print(out)
        reply = out
    elif 'rest' in command or 'sleep' in command:
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        exit()
    else:
        show_msg(dict(
            {'name': 'Jarvis', 'msg': "I can search the web for you, Do you want to continue?"}))
        root.update()
        talk("I can search the web for you, Do you want to continue?")
        while(True):
            ans = first_1()
            if ans['msg'] != "":
                break
        show_msg(ans)
        root.update()
        ans = ans['msg']
        if 'yes' in str(ans) or 'yeah' in str(ans):
            pywhatkit.search(command)
            reply = "ok sir!! i have searched what i cannot understand !!"
        else:
            reply = 'sorry sir!! i cannot understand !!!'

    return dict({"name": "Jarvis", "msg": reply})

def postevent(titleentry, descentry, startentry, endentry, phone_window):
    event = {
        'summary': '',
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
    create_event(event)
    talk("Event created successfully and added to google calendar")
    delete_window()
    create_window()
    get_va_msg()


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-")+"-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(['notepad.exe', file_name])


def run_note():
    talk("What would you like me to write down?")
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What would you like me to write down?"}))
    root.update()
    while True:
        note_text = first_1()
        if(note_text['msg'] != ""):
            break
    note(note_text['msg'])
    show_msg(dict({'name': 'Jarvis', 'msg': "I've made a note of that."}))
    root.update()
    delete_window()
    create_window()
    get_va_msg()


def weather():
    api_key = "d97dd2dfd8d75bd9862f7f4e71096463"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What is the city name"}))
    root.update()
    talk("What is the city name?")
    while True:
        city_name = first_1()
        if(city_name['msg'] != ""):
            break
    show_msg(city_name)
    root.update()
    parm = {'APPID': api_key, 'q': city_name['msg'], 'units': 'Metric'}
    response = requests.get(base_url, params=parm)
    weather = response.json()
    if weather["cod"] != "404":
        reply = "Name: "+str(weather['name']) + "\n"
        reply += "Conditions: " + \
            str(weather['weather'][0]['description']) + "\n"
        reply += "Temperature in celsius:"+str(weather['main']['temp'])
    else:
        reply = "City Not Found"
    show_msg(dict({'name': 'Jarvis', 'msg': reply}))
    root.update()
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
    talk("Verify the event details")


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
        talk(e)
        delete_window()
        create_window()
        get_va_msg()
    utc = pytz.UTC
    # checkdetailswindow(
    #     "jarvis testing", "jarvis testing", "5.00pm", "6.00pm")
    show_msg(dict({'name': 'Jarvis', 'msg': 'What is the event title sir?'}))
    root.update()
    talk('What is the event title sir?')
    while (True):
        event_title = first_1()
        if event_title['msg'] != "":
            break
    show_msg(event_title)
    root.update()
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'Would u like to add any description of the event?'}))
    root.update()
    talk('Would u like to add any description of the event?')
    while (True):
        event_description = first_1()
        if event_description['msg'] != "":
            break
    show_msg(event_description)
    root.update()
    if event_description['msg'] == "no":
        event_description['msg'] = ""
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'What is the event start time?'}))
    root.update()
    talk('What is the event start time?')
    while (True):
        start_time = first_1()
        if start_time['msg'] != "":
            starttime = timdefromtext(start_time)
            starttime = str(date)+"T"+starttime
            print(starttime)
            break
    show_msg(start_time)
    root.update()
    show_msg(dict(
        {'name': 'Jarvis', 'msg': 'What is the event end time?'}))
    root.update()
    talk('What is the event end time?')
    while (True):
        end_time = first_1()
        if end_time['msg'] != "":
            endtime = timdefromtext(end_time)
            endtime = date+'T'+str(endtime)
            print(endtime)
            break
    show_msg(end_time)
    root.update()
    checkdetailswindow(
        event_title['msg'], event_description['msg'], starttime, endtime)


def sendwhatsappmsg(ph_no, phonewindow):
    if phonewindow != None:
        phonewindow.destroy()
    show_msg(dict({'name': 'You', 'msg': ph_no}))
    show_msg(dict({'name': 'Jarvis', 'msg': "What is the message?"}))
    root.update()
    talk("What is the message?")
    note_text = first_1()
    show_msg(note_text)
    root.update()
    a = 1
    if(a == 59 and int(datetime.datetime.now().strftime("%S")) <= 40):
        a = 0
    talk("Your message will be sent shortly to "+ph_no)
    show_msg(
        dict({'name': 'Jarvis', 'msg': "Your message will be sent shortly to "+ph_no}))
    root.update()
    try:
        pywhatkit.sendwhatmsg(f"+91{ph_no}", note_text['msg'], int(datetime.datetime.now(
        ).strftime("%H")), int(datetime.datetime.now().strftime("%M"))+a, wait_time=10)
    except pywhatkit.exceptions.CallTimeException:
        talk("Message took long time to send. Please try again")
        show_msg(dict(
            {'name': 'Jarvis', 'msg': "Message took long time to send. Please try again"}))
        time.sleep(1)
        delete_window()
        create_window()
        sendwhatsappmsg(ph_no, phonewindow)
    delete_window()
    create_window()
    get_va_msg()


def sendmail(ph_no, phonewindow):
    phonewindow.destroy()
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What is the subject?"}))
    root.update()
    talk("What is the subject?")
    sub = first_1()
    show_msg(sub)
    root.update()
    show_msg(
        dict({'name': 'Jarvis', 'msg': "What is the message?"}))
    root.update()
    talk("What is the message?")
    note_text = first_1()
    show_msg(note_text)
    root.update()
    pywhatkit.send_mail("socialmediaatwork123@gmail.com",
                        "Qwerty123@", sub['msg'], note_text['msg'], ph_no)
    show_msg(
        dict({'name': 'Jarvis', 'msg': "Email sent successfully to "+ph_no}))
    root.update()
    talk("Email sent successfully to "+ph_no)
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
    talk("Enter the Email address")


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
    talk("Enter the Phone Number")


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
    msg = first_1()
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
        date = get_date(msg['msg'])
        createevent_google(date)
    elif 'rest' in msg['msg'] or 'sleep' in msg['msg']:
        show_msg(msg)
        root.update()
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        show_msg(dict(
            {'name': "Jarvis", 'msg': "Okay Guys I will just take a nap, Call me whenever u need my help"}))
        root.update()
        talk(reply)
        time.sleep(1)
        exit()
    elif "weather" in msg['msg']:
        show_msg(msg)
        root.update()
        weather()
    elif 'make a note' in msg['msg'] or 'open notepad' in msg['msg'] or 'write this down' in msg['msg']:
        show_msg(msg)
        root.update()
        run_note()
    else:
        show_msg(msg)
        root.update()
        changesatus("Processing..")
        root.update()
        msg = run_alexa(msg['msg'])
        show_msg(msg)
        root.update()
        talk(msg['msg'])
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
    else:
        msgframe = Frame(frame1, bg='gray26')
        newmsg = Label(msgframe, text=msg['msg'], font=(
            "Georgia"), wraplength=200, padx=10, justify=LEFT)
        msgframe.pack(side=TOP, fill=X, pady=10, padx=10)
        newmsg.pack(side=LEFT)


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
img = Image.open("avatar.jpg")
img = img.resize((50, 50))
avatarimg = ImageTk.PhotoImage(img)
avatarframe = Frame(frame1, bg='gray26')
avatar = Label(avatarframe, image=avatarimg, anchor=E,
               height=50, width=50, padx=5, pady=5, bg="gray26", justify=RIGHT)
avatarframe.pack(side=TOP, pady=10, fill=X, padx=10)
avatar.pack(side=RIGHT, pady=10)
root.resizable(0, 0)
msg = first_run()
show_msg(msg)
root.update()
talk(msg['msg'])
get_va_msg()
root.mainloop()
