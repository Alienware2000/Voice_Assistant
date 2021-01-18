import speech_recognition as sr
import webbrowser
import wolframalpha
import wikipedia
import playsound
import os
import random
import smtplib
import ssl
from email.message import EmailMessage
from translate import Translator
from gtts import gTTS

# Wolfram alpha API client
app_id = 'RHERLV-LWX6LJT6PW'
client = wolframalpha.Client(app_id)

# An instance of the recognizer class
r = sr.Recognizer()


# Obtain audio from the microphone
def listen(ask=None):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)

        if ask:
            speak(ask)

        audio = r.listen(source)
        audio_data = ''

        try:
            audio_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that. Please try again")
        except sr.RequestError:
            speak("Sorry, My speech service is down")

    return audio_data


# This function converts text into speech
def speak(audio, lang='en-us'):
    tts = gTTS(text=audio, lang=lang)
    rand = random.randint(1, 10000000)
    audio_file = 'audio-' + str(rand) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)
    print(audio)


# Just by saying language, you get to call this function which allows you to translate to french or spanish
def translate():
    trnslate = listen("Which language do you want to translate to? French or Spanish")
    if trnslate == 'French' or trnslate == 'Spanish':
        text = listen("What do you want to say?")
        if trnslate == 'French':
            speak(Translator(to_lang='fr', from_lang='en').translate(text), lang='fr')
        elif trnslate == 'Spanish':
            speak(Translator(to_lang='es', from_lang='en').translate(text), lang='es')
    else:
        speak("Sorry, you can only choose french or spanish. More languages will come soon")


# This function is responsible for sending an email to a user on gmail
def send_email():
    speak("Who do  you want to send an email to?")
    recipient = input()
    recipient_address = recipient + '@gmail.com'

    subject = listen("What is your subject?")
    content = listen("What do you want to send?")

    email_address = input('Email Address: ')
    email_password = input('Password: ')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient_address
    msg.set_content(content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


# This finds any location you give it to find on Google Maps
def find_location():
    find = listen("Which location do you want to find?")
    url = 'https://www.google.com/maps/place/' + find + '/&amp'
    webbrowser.open(url)
    speak(f"Here is the gps location of {find}")


# This allows you to check wikipedia and gives you a summary of a topic
def check_wiki():
    wiki = listen("What do you want to wiki search for?")
    answer = wikipedia.summary(wiki, sentences=5)
    speak(answer)


# This allows you to open your web browser and search for almost anything
def search():
    google = listen("What do you want to search for?")
    url = 'https://www.google.com/search?q=' + google
    webbrowser.open(url)
    speak("Here is what I found")


# This is the function that basically gives you back a response ,as the name implies, to the listen function
def respond(voice_data):
    if voice_data == 'exit':
        exit()

    if 'your name' in voice_data:
        speak("Hi, My name is Alexa")
    elif voice_data == 'search':
        search()
    elif voice_data == 'find location':
        find_location()
    elif voice_data == 'check wiki':
        check_wiki()
    elif voice_data == 'send email':
        send_email()
    elif voice_data == 'language':
        translate()
    else:
        try:
            res = client.query(voice_data)
            answer = next(res.results).text
            speak(answer)
        except:
            speak("Sorry I didn't quite get that")


speak("Hi, my name is Alexa. How can I help you?")

# To keep running the Voice assistant till exit is said by the user
while True:
    voice_data = listen()
    respond(voice_data)
    speak("How can I help you?")


