# -*- coding: utf-8 -*-
"""
Created on Sun May 30 11:02:31 2021
@author: Ashish
"""

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import subprocess
# import ashishui as ui

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def first_run():
    welcome_msg = "HI Project Members This is Jarvis here!!.Current time is {}. An exciting day awaits before you .!!".format(
        datetime.datetime.now().strftime('%I:%M %p'))
    # engine.say("HI Project Members This is Jarvis here!!.Current time is {}. An exciting day awaits before you .!!".format(
    #     datetime.datetime.now().strftime('%I:%M %p')))
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
                voice, key=None, language ='en-in', show_all=True)
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
    file_name = str(date).replace(":","-")+"-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    
    subprocess.Popen(['notepad.exe',file_name])        
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
        if(len(ph_no)==10 and ph_no.isnumeric() == True):
            break
    
    talk("What is the message?")
    note_text = first_1()
    a=1
    if(a==60 and int(datetime.datetime.now().strftime("%S")) <= 40):
        a=0
    
    pywhatkit.sendwhatmsg(f"+91{ph_no}",note_text['msg'],int(datetime.datetime.now().strftime("%H")),int(datetime.datetime.now().strftime("%M"))+a,wait_time=10)

    return "I've sent the message to this phone number :"+ph_no



def run_alexa(command):
    if command == "No command recieved":
        reply = "No command recieved"
    elif 'play' in command:
        song = command.replace('play', '')
        # talk('playing ' + song)
        reply = 'playing ' + song
        pywhatkit.playonyt(song)
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
    elif 'open notepad' in command:
        reply = run_note()
    elif 'make a note' in command:
        reply = run_note()
    elif 'write this down' in command:
        reply = run_note()
    elif 'send a message in whatsapp' in command:
        reply = whats_run()
    elif 'rest' in command or 'sleep' in command:
        # talk('Okay Guys I will just take a nap, Call me whenever u need my help')
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        exit()
    else:
        # talk('Please say the command again.')
        reply = 'Please say the command again.'

    return dict({"name": "Jarvis", "msg": reply})


# if __name__ == "__main__":
#     app = ui.ChatApplication()
#     while(True):
#         app.run()
#         run_alexa(app)
