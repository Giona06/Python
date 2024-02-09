import speech_recognition as sr
from commands import Recognize_Command

recognizer_instance = sr.Recognizer() # Crea una istanza del recognizer
try:
    while(True):
        with sr.Microphone() as source:
            recognizer_instance.adjust_for_ambient_noise(source)
            print("Sono in ascolto... parla pure!")
            audio = recognizer_instance.listen(source)
            try:
                text = recognizer_instance.recognize_google(audio, language='it-IT')
                Recognize_Command(text)
            except Exception as e:
                print("Errore nell'ascolto")
                print(e)
except(BaseException):
        print("Fine dell'ascolto, chiusura del programma")