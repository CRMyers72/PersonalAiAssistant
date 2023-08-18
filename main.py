import numpy as np
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", "voices[1].id")

aiName = "Charlotte"


# This function converts text to speech and returns back when all commands queded before tis call are emptied from the queue
def speak(text):
    engine.say(text)
    engine.runAndWait()


# simple function that generates a greeting based off of the current time
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello and Good Morning")
        print("Hello and Good Morning")
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        speak("Good Evening")
        print("Good Evening")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language="en-in")
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("I didn't get that, please say that again")
            return "None"
        return statement


print(f"Loading {aiName}, your personal assistant")
speak(f"Loading {aiName}, your personal assistant")
wishMe()

if __name__ == "__main__":
    while True:
        speak("Tell me how I can help you now?")
        statement = takeCommand().lower()
        if statement == 0:
            continue
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak(f"{aiName} is shutting down, Good bye")
            print(f"{aiName} is shutting down, Good bye")
            break
        if "wikipedia" in statement:
            speak("searching Wikipedia")
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "open youtube" in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is open")
            time.sleep(5)
        elif "open google" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is now open")
            time.sleep(5)
        elif "open outlook" in statement:
            webbrowser.open_new_tab("outlook.com")
            speak("Outlook is open")
            time.sleep(5)
        elif "time" in statement:
            strTime = datetime.satetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "news" in statement:
            news = webbrowser.open_new_tab("https://ground.news")
            speak("Here's the news")
            time.sleep(6)
        elif "camera" in statement or "take photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")
        elif "search" in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)
        elif "weather" in statement:
            api_key = ""
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(
                    " Temperature in kelvin unit is "
                    + str(current_temperature)
                    + "\n humidity in percentage is "
                    + str(current_humidiy)
                    + "\n description  "
                    + str(weather_description)
                )
                print(
                    " Temperature in kelvin unit = "
                    + str(current_temperature)
                    + "\n humidity (in percentage) = "
                    + str(current_humidiy)
                    + "\n description = "
                    + str(weather_description)
                )

            else:
                speak(" City Not Found ")
        elif "ask" in statement:
            speak(
                "I can answer to computational and geographical questions and what question do you want to ask now"
            )
            question = takeCommand()
            app_id = "LJ939P-H62AKQWKKJ"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "log off" in statement or "sign out" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications"
            )
            subprocess.call(["shutdown", "/l"])
time.sleep(3)
