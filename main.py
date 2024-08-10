import datetime
import os
import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import time as ti
import webbrowser as we
from time import sleep
import random


# Set the variables for user name and assistant name 
user = "Neha"
assistant = "Jarvis" 

# Set up pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty("voices")

# For Male voice AKA Jarvis
engine.setProperty("voice", voices[0].id)

# Input and output functions

def get_study_tips():
    tips = [
        "Create a study schedule and stick to it.",
        "Take regular breaks to avoid burnout.",
        "Use flashcards to memorize important concepts.",
        "Teach someone else what you've learned to reinforce your knowledge.",
        "Stay hydrated and get enough sleep."
    ]
    return random.choice(tips)

def generate_quiz_question():
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Rome", "Berlin"],
            "answer": "Paris"
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H2O", "CO2", "NaCl", "O2"],
            "answer": "H2O"
        },
        {
            "question": "What is the largest planet in our solar system?",
            "options": ["Earth", "Jupiter", "Mars", "Saturn"],
            "answer": "Jupiter"
        }
    ]
    question = random.choice(questions)
    return question

def quiz():
    # Get a quiz question
    question = generate_quiz_question()
    output(f"Question: {question['question']}\nOptions: {', '.join(question['options'])}")
    
    # Wait for user's answer
    output("Please provide your answer.")
    user_answer = inputCommand().strip()

    # Check if the answer is correct
    if user_answer.lower() == question['answer'].lower():
        output("Correct! Well done.")
    else:
        output(f"Wrong. The correct answer is {question['answer']}.")


def sendWhatMsg():
    user_name = {
        'Neha': '+91 63625 61084'
    }
    try:
        output("To whom you want to send the message?")
        name = inputCommand()
        if name in user_name:
            output("What is the message?")
            message = inputCommand()
            pywhatkit.sendwhatmsg_instantly(user_name[name], message, 10, True, 2)
            output("Message sent")
        else:
            output("Contact not found.")
    except Exception as e:
        print(e)
        output("Unable to send the message")

def output(audio):
    print(audio) 
    engine.say(audio)
    engine.runAndWait()
    

def inputCommand():
    r = sr.Recognizer()
    query = ""
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Adjusted pause threshold for faster response
        r.energy_threshold = 300  # Set energy threshold for ambient noise levels
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)  # Add timeout and phrase_time_limit
            query = r.recognize_google(audio, language="en-IN")
        except sr.WaitTimeoutError:
            output("Listening timed out, please try again.")
        except sr.UnknownValueError:
            output("Could not understand audio, please try again.")
        except sr.RequestError:
            output("Could not request results, please check your internet connection.")
        except Exception as e:
            output("Say that again please...")
            print(e)
    return query.lower()

# Greet function
def greet():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        output(f"Good Morning {user}")
    elif 12 <= hour < 18:
        output(f"Good Afternoon {user}")
    elif 18 <= hour < 21:
        output(f"Good Evening {user}")
    else:
        output(f"Hello {user}")
    output("How may I assist you?")


# Weather function
def weather():
    city = "bangalore"
    try:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=678ad86ef9b05fb792f276f3d17156ca&units=metric").json()
        temp1 = res["weather"][0]["description"]
        temp2 = res["main"]["temp"]
        output(f"Temperature is {temp2} degree Celsius \nWeather is {temp1}")
    except Exception as e:
        print(e)
        output("Unable to retrieve weather information.")


# Idea function
def idea():
    output("What is your idea?")
    data = inputCommand().title()
    output(f"You said me to remember this idea: {data}")
    with open("data.txt", "a", encoding="utf-8") as r:
        r.write(f"{data}\n")

# Greet and main loop
greet()
while True:
    query = inputCommand()
    
    if "time" in query:
        output("Current time is " + datetime.datetime.now().strftime("%I:%M %p"))

    elif "date" in query:
        output("Current date is " + datetime.datetime.now().strftime("%d %B %Y"))


    elif "search" in query:
        output("What do you want to search?")
        search_query = inputCommand()
        we.open("https://www.google.com/search?q=" + search_query)

    elif "youtube" in query:
        output("What do you want to search on YouTube?")
        pywhatkit.playonyt(inputCommand())

    elif "weather" in query:
        weather()
              
    elif "joke" in query:
        output(pyjokes.get_joke())

    elif "idea" in query:
        idea()

    elif "quiz" in query:
        quiz()

    elif "screenshot" in query:
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{ti.time()}.png")
        output("Screenshot taken")

       
    elif "study tips" in query:
        tip = get_study_tips()
        output(tip)
        
    elif "quiz" in query:
        question = generate_quiz_question()
        output(question)

    elif "cpu" in query:
        output(f"CPU is at {psutil.cpu_percent()}%")

    elif "my name" in query:
        output(f"Your name is {user}")

    elif "who are you" in query:
        output(f"I am {assistant}")

    elif "goodbye" in query:
        hour = datetime.datetime.now().hour
        if 21 <= hour or hour < 6:
            output(f"Good Night {user}! Have a nice sleep.")
        else:
            output(f"Goodbye {user}")
        break
