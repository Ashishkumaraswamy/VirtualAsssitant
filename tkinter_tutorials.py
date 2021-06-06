# -*- coding: utf-8 -*-
"""
Created on Sun May 30 11:02:31 2021
@author: Ashish
"""
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import subprocess
import pyscreenshot
import pytz
import webbrowser
import psutil
from PyDictionary import PyDictionary


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
dictionary=PyDictionary()

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


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

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
                    except:
                        pass

    # THE NEW PART STARTS HERE
    # if the month mentioned is before the current month set the year to the next
    if month < today.month and month != -1:
        year = year+1

    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)


def first_run():
    welcome_msg = "HI Project Members This is Jarvis here!!.Current time is {}. An exciting day awaits before you .!!".format(
        datetime.datetime.now().strftime('%I:%M %p'))
    engine.runAndWait()
    return dict({'name': 'Jarvis', 'msg': welcome_msg})


def talk(text):
    engine.say(text)
    engine.runAndWait()


# # def take_command():
# #     try:
# #         with sr.Microphone() as source:
# #             print('listening...')
# #             voice = listener.listen(source)
# #             command = listener.recognize_google(voice)
# #             command = command.lower()
# #             if 'alexa' in command:
# #                 command = command.replace('alexa', '')
# #                 print(command)
# #     except:
# #         pass
# #     return command


# # def run_alexa():
# #     command = take_command()
# #     print(command)
# #     if 'play' in command:
# #         song = command.replace('play', '')
# #         talk('playing ' + song)
# #         pywhatkit.playonyt(song)
# #     elif 'time' in command:
# #         time = datetime.datetime.now().strftime('%I:%M %p')
# #         talk('Current time is ' + time)
# #     elif 'who the heck is' in command:
# #         person = command.replace('who the heck is', '')
# #         info = wikipedia.summary(person, 1)
# #         print(info)
# #         talk(info)
# #     elif 'date' in command:
# #         talk('sorry, I have a headache')
# #     elif 'are you single' in command:
# #         talk('I am in a relationship with wifi')
# #     elif 'joke' in command:
# #         talk(pyjokes.get_joke())
# #     else:
# #         talk('Please say the command again.')


def first_1():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            # print(voice.get_raw_data())
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


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-")+"-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(['notepad.exe', file_name])


def run_note():
    talk("What would you like me to write down?")
    note_text = first_1()
    note(note_text['msg'])
    return "I've made a note of that."


def whats_run():
    while(True):
        talk("can you tell the mobile number?")
        ph_no = first_1()
        ph_no = ph_no['msg']
        ph_no = ph_no.replace(' ', '')
        print(ph_no)
        if(len(ph_no) == 10 and ph_no.isnumeric() == True):
            break

    talk("What is the message?")
    note_text = first_1()
    a = 1
    if(a == 60 and int(datetime.datetime.now().strftime("%S")) <= 40):
        a = 0

    pywhatkit.sendwhatmsg(f"+91{ph_no}", note_text['msg'], int(datetime.datetime.now(
    ).strftime("%H")), int(datetime.datetime.now().strftime("%M"))+a, wait_time=10)

    return "I've sent the message to this phone number :"+ph_no


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
        # talk('searching ' + inp)
        reply = 'searching ' + inp
        pywhatkit.search(inp)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        reply = 'Current time is ' + time
        # talk('Current time is ' + time)
    elif 'tell me about' in command:
        person = command.replace('tell me about', '')
        reply = wikipedia.summary(person, 1)
    elif 'joke' in command:
        reply = pyjokes.get_joke()
    elif 'play' in command:
        song = command.replace('play', '')
        reply = 'playing ' + song
        pywhatkit.playonyt(song)
    elif 'battery percentage' in command or 'battery info' in command or 'battery information' in command :
        battery_data = psutil.sensors_battery()
        if battery_data.power_plugged:
            strg = ' charging '
        else:
            strg = ' not charging '
        reply = "Your system is currently "+strg+"and it is "+format(battery_data.percent)+" percent."

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
    elif 'open notepad' in command:
        reply = run_note()
    elif 'open spotify' in command:
        subprocess.Popen(['spotify.exe'])
        reply = "Opened Spotify application"
    elif 'make a note' in command:
        reply = run_note()
    elif 'write this down' in command:
        reply = run_note()
    
    elif 'open myanimelist' in command or 'open stackoverflow' in command or 'open youtube' in command or 'open github' in command or 'open nucleus' in command or 'open moodle' in command :
        inp = command.replace('open', '')
        inp = inp.replace(' ', '')
        talk("Opening "+inp+" Sir!!")
        b=webbrowser.get()
        if( inp == "myanimelist"):
            b.open("https://myanimelist.net")
        elif ( inp == "stackoverflow"):
            b.open("https://stackoverflow.com")
        elif ( inp == "youtube"):
            b.open("https://www.youtube.com")
        elif ( inp == "github"):
            b.open("https://github.com")
        elif ( inp == "nucleus"):
            b.open("https://nucleus.amcspsgtech.in")
        elif ( inp == "moodle"):
            b.open("https://moodle.amcspsgtech.in")
        reply = "Opened "+inp+" in your web browser"


    elif 'open spotify' in command:
        talk("Opening Spotify Sir!!")
        subprocess.Popen(['spotify.exe'])
        #subprocess.run(['spotify.exe'],input="dive back in time",)
        # b=webbrowser.get()
        # b.open("https://open.spotify.com")  
        reply = "Opened Spotify application"


    elif 'send a message in whatsapp' in command:
        reply = whats_run()
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
        # talk('Okay Guys I will just take a nap, Call me whenever u need my help')
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        exit()
    else:
        # talk('Please say the command again.')
        reply = 'sorry sir!! i cannot understand !!!'

    return dict({"name": "Jarvis", "msg": reply})



run_alexa("find the meaning of nonsense")
# if __name__ == "__main__":
#     app = ui.ChatApplication()
#     while(True):
#         app.run()
#         run_alexa(app)
