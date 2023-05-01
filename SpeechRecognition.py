import smtplib
import subprocess
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyaudio

engine=pyttsx3.init()
voices=engine.getProperty("voices")
newVoiceRate = 145
engine.setProperty('rate',newVoiceRate)
engine.setProperty("voice",voices[1].id)
def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            str="Heyy i am python assistant what can i do for you"
            talk(str)
            listener.pause_threshold = 1
            print("speak....")
            voice=listener.listen(source)
            name=listener.recognize_google(voice)
            command = listener.recognize_google(voice)
            print(command)
            #talk(command)
    except:
        print("exception occured")
    return command

def running():
    command = take_command()
    if "play" in command:
        cur=command.replace("play","")
        talk("playing"+cur)
        pywhatkit.playonyt(cur)
    elif "Mouse controls" in command:
        try:
            print("mouse controls activated")
            subprocess.run(["python", "./virtualmouse.py"])
        except:
            print("exception in mouse controls activation")
    elif "Activate scroll" in command or "scroll" in command or "school" in command:
        try:
            print("mouse controls activated")
            subprocess.run(["python", "./AutoScroll.py"])
        except:
            print("exception in Scrolling Activation")
    elif "activate controls" in command:
        try:
            print(" controls activated")
            subprocess.run(["python", "./main.py"])
        except:
            print("expection in activating system controls")
    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif "who" in command:
        search = command.replace('who is', '')
        info = wikipedia.summary(search, 1)
        talk(info)
    elif "send" in command:
        talk("Enter phone number with country code: ")
        p=input()
        talk("Enter your message:")
        m=input()
        talk("Enter time in hours:")
        h=int(input())
        talk("Enter time in minutes: ")
        min=int(input())
        pywhatkit.sendwhatmsg(p,m,h,min)
    elif "goodbye":
        talk("Bye")
    else:
        talk("I am sorry.I cant hear you")


while True:
    running()