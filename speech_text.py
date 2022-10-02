import pyttsx3
engine = pyttsx3.init('sapi5')           
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  #male(0) or female(1) 
engine.setProperty('rate', 110)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


