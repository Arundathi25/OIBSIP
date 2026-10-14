import speech_recognition as sr
import pyttsx3
import subprocess

# Create Voice Assistant
engine = pyttsx3.init()


def speak(text: str) -> None:
    print("Assistant:", text)

    safe_text = text.replace('"', '""')

    command = (
        'Add-Type -AssemblyName System.Speech; '
        '$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speaker.Speak("{safe_text}"); '
        '$speaker.Dispose()'
    )

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=False
    )


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please try again.")
        return ""

    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the speech service.")
        return ""


speak("Hello Chinny, I can speak to you. I'm your voice assistant.")

while True:
    command = listen()

    if "what is your name" in command:
        speak("Hi Chinny, I'm your voice assistant.")

    elif "how can you help me" in command:
        speak("I can listen to your questions and give you spoken answers.")

    elif "what can you do for me" in command:
        speak("I can listen to your voice commands, answer your questions, and speak my responses.")

    elif "say thank you bye" in command or "thank you bye" in command:
        speak("Chinny, thank you, goodbye, have a nice day.")
        break

    elif command:
        speak("Sorry, I don't have an answer for that command.")
