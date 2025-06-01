
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # Make sure this is a Python file with a `music` dictionary
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
newsapi = os.getenv("NEWSAPI_KEY")
openaiapi = os.getenv("OPENAIAPI_KEY")



# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Optional: set voice rate (speed)
engine.setProperty('rate', 150)

def aiProcess(command):
  
    client = OpenAI(api_key= openaiapi )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
     messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
     ]
     )

    return completion.choices[0].message.content


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play "):
        song = command[5:]  # get song after "play " skip 5 character
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")
    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

      
        if r.status_code == 200:
        #    parse the json response
            data= r.json()
           

            # Extract the article
            articles =data.get('articles', [])

            # print the headline
            speak("Here are the top 5 news headlines:")
            for  article in articles[:4]:
                speak(f"{article['title']}")

       
    else:
            # Let OpenAI handle the request
            output = aiProcess(command)
            speak(output) 

def listen_for_speech(timeout, phrase_time_limit):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return recognizer.recognize_google(audio)



if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            print("Say 'Jarvis' to activate...")
            trigger = listen_for_speech(timeout=5, phrase_time_limit=2)

            if "jarvis" in trigger.lower():
                speak("Yes?")
                try:
                    command = listen_for_speech(timeout=5, phrase_time_limit=6)
                    print(command)
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that. Try again.")
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            speak("Could not request results; check your internet connection.")
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error: {e}")

