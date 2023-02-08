#https://electronoobs.com/eng_arduino_tut171.php
#pip install SpeechRecognition
#sudo apt install pyaudio
#pip install sounddevice


import sounddevice
import serial
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("Start talking!")

while True:
    with mic as source:
        audio = r.listen(source)
    words = r.recognize_google(audio)
    print(words)