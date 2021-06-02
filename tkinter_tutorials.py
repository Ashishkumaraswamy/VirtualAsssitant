# -*- coding: utf-8 -*-
"""
Created on Sun May 30 11:02:31 2021
@author: Ashish
"""

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
# import ashishui as ui

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def first_run():
    engine.say("HI Project Members This is Jarvis here!!.Current time is {}. An exciting day awaits before you .!!".format(
        datetime.datetime.now().strftime('%I:%M %p')))
    engine.runAndWait()


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


# # while True:
# #     run_alexa()


def first_1():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            talk('listening...')
            voice = listener.listen(source)
            # print(voice.get_raw_data())
            command = listener.recognize_google(
                voice, key=None, language='en-US', show_all=True)
            if command != []:
                command = command['alternative'][0]['transcript']
                command = command.lower()
                talk(command)
            else:
                command = "No command recieved"
                talk(command)
    except:
        pass
    return dict({"name": "You", "msg": command})


def run_alexa(command):
    if command == "No command recieved":
        reply = "No command recieved"
    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        reply = 'playing ' + song
        pywhatkit.playonyt(song)
    elif 'search' in command:
        inp = command.replace('search', '')
        talk('searching ' + inp)
        reply = 'searching ' + inp
        pywhatkit.search(inp)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        reply = 'Current time is ' + time
        talk('Current time is ' + time)
    elif 'rest' in command or 'sleep' in command:
        talk('Okay Guys I will just take a nap, Call me whenever u need my help')
        reply = 'Okay Guys I will just take a nap, Call me whenever u need my help'
        exit()
    else:
        talk('Please say the command again.')
        reply = 'Please say the command again.'

    return dict({"name": "Jarvis", "msg": reply})


# if __name__ == "__main__":
#     app = ui.ChatApplication()
#     while(True):
#         app.run()
#         run_alexa(app)
