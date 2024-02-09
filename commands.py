from os import system
import subprocess

webbrowser_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"     #path per il browser, utile per i vari comandi che usano google
stopcommands = ["ferma" , "stop" , "basta", "chiudi"]   #varie opzioni per chiudere 
startcommands = ["avvia", "apri", "start"]              #e aprire le applicazioni

processes = {}  #dizionario che tiene traccia di tutti i processi aperti dal programma

def Recognize_Command(text):
    system('cls')
    print(text)     #print di quello che ha sentito in input
    text = str(text).lower()    #tutto lowercase che ci piace
    if(any(word in text for word in startcommands)):    #tutti i comandi che cominciano con apri, avvia, ecc...
        if("google" in text):
            processes.update({"google" : subprocess.Popen(webbrowser_path)})
        
        elif("visual studio" in text):
            processes.update({"vscode" : subprocess.Popen("C:\\Users\\stage\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe")})
        
        elif("youtube" in text):
            processes.update({"youtube" : subprocess.Popen([webbrowser_path, "https://www.youtube.com"])})
        
        elif("classificazione audio" in text):
            if("noise" not in processes):
                processes.update({"noise" : subprocess.Popen("C:/Users/stage/Desktop/test/dist/test.exe", creationflags = subprocess.CREATE_NEW_CONSOLE)})      #senza la flag il processo parte nel terminale di vscode
            else:
                print("Il processo è già aperto")
        elif("impostazioni" in text):
             processes.update({"settings" : subprocess.Popen(["start", "ms-settings:"])})
    elif(any(word in text for word in stopcommands)):   #tutti i comandi che cominciano con chiudi, stop, ecc...
        
        if("google" in text):
            if("google" in processes):
                processes.get("google").terminate()
                del processes["google"]
            else:
                print("Il processo non esiste")

        elif("vscode" in text):
            if("vscode" in processes):
                processes.get("vscode").terminate()
                del processes["vscode"]
            else:
                print("Il processo non esiste")
        
        elif("youtube" in text):
            if("youtube" in processes):
                processes.get("youtube").terminate()
                del processes["youtube"]
            else:
                print("Il processo non esiste")
        
        elif("classificazione audio" in text):
            if("noise" in processes):
                processes.get("noise").terminate()
                del processes["noise"]
            else:
                print("Il processo non esiste")
        
        elif("impostazioni" in text):
            if("impostazioni" in processes):
                processes.get("impostazioni").terminate()
                del processes["impostazioni"]
            else:
                print("Il processo non esiste")
        else:
            raise SystemExit(0)
    
    if("spegni" in text):
            system("shutdown /s /t 1")
    
    if("riccardo rotola" in text):
            s = subprocess.run([webbrowser_path, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"])
    
    
    
          

    
