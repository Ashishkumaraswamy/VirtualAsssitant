from __future__ import print_function
from copy import error
import datetime
import os.path
import sys
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
import gui


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
        gui.show_msg(dict(
            {'name': 'Jarvis', 'msg': "I can search the web for you, Do you want to continue?"}))
        gui.root.update()
        talk("I can search the web for you, Do you want to continue?")
        while(True):
            ans = first_1()
            if ans['msg'] != "":
                break
        gui.show_msg(ans)
        gui.root.update()
        ans = ans['msg']
        if 'yes' in str(ans) or 'yeah' in str(ans):
            pywhatkit.search(command)
            reply = "ok sir!! i have searched what i cannot understand !!"
        else:
            reply = 'sorry sir!! i cannot understand !!!'

    return dict({"name": "Jarvis", "msg": reply})
