
import sys
import time
from pymata4 import pymata4
import pyttsx3
engine = pyttsx3.init('sapi5')           
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  #male(0) or female(1) 
engine.setProperty('rate', 110)

def speak(audio):
    while(audio):

        engine.say(audio)
        engine.runAndWait()

triggePin = 11
echo_pin = 12

board = pymata4.Pymata4()


def the_callback(data):

        if data[2] > 50:
                print("go")
        else:
                speak("Stop, Obstacle ahead")
                
                

board.set_pin_mode_sonar(triggePin, echo_pin, the_callback)
while True:
        try:
                time.sleep(1)
                board.sonar_read(triggePin)
        except KeyboardInterrupt:
                board.shutdown()
                sys.exit(0)