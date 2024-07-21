import pyautogui
import webbrowser
import os
from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr
import winsound
from datetime import datetime

# First listen to the given command and convert to text
def listen():
    recognizer = sr.Recognizer

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google_cloud(audio)
        print("I heard: ", command)
        return command.lower()
    except sr.UnknownValueError:
        print("I was unable to understand the command. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API")
        return None

# An audio response using gtts
def respond(answer):
    print(answer)
    voice = gTTS(text=answer, lang='en')
    voice.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)

# Function to carry out specific tasks.
task_list = []
listening = False

def main():
    global task_list
    global listening
    VA_name = "Space Crab"

    while True:
        command = listen()

        if command and VA_name in command:
            if listening:
                task_list.append(command)
                listening = False
                respond("Added" + command + "to your task list")
            elif "add a task" in command:
                respond("What is the task?")
                listening = True
            elif "clear the task list" in command:
                task_list.clear()
                respond("Task list cleared")
            elif "time" in command:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                respond("The time is" + current_time)
            elif "open chrome" in command:
                respond("Opening Chrome")
                webbrowser.open('https://www.google.com/')
            elif "open whatsapp" in command:
                respond("Opening WhatsApp")
                os.system("WhatsApp")
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I have taken a screenshot")
            elif "close" in command:
                respond("Goodbye")
                break
            else:
                respond("Sorry I can't handle that command")

if __name__ == '__main__':
    main()

