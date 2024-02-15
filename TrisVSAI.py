from os import system
from model import azioni_disponibili_da_stringa
from model import scegli_azione
from model import esegui_mossa
from model import aggiorna_q_table

gameboard = {
        "1" : None, "2" :None, "3" : None,
        "4" : None, "5" : None, "6" : None,
        "7" : None, "8" : None, "9" : None
    }

i = 0

playerChar = "X"

Q_tableO = {}

def UpdateTableFile():
    with open('qtableo.txt', 'w') as file:
        for key, value in Q_tableO.items():
            file.write(f'{key}:{value}\n')

with open('qtableo.txt', 'r') as file:
        input_string = file.readline()
        # Separazione della stringa del dizionario e del float
        dict_string, float_string = input_string.split('):')
        # Rimozione delle parentesi dalla stringa del dizionario
        dict_string = dict_string[1:]
        # Creazione del dict con il dizionario convertito e il float
        Q_tableO[eval(dict_string)] = float(float_string)

def Reset():
    global gameboard
    gameboard = {
        "1" : None, "2" :None, "3" : None,
        "4" : None, "5" : None, "6" : None,
        "7" : None, "8" : None, "9" : None
    }
    global i 
    i = 0
    return gameboard

def FillMatrix():
    global i
    foundValidPosition = False
    while not foundValidPosition:
        n = input()
        if gameboard[n] is None:
            gameboard[n] = "X"
            foundValidPosition = True
            i += 1
        else:
            foundValidPosition = False
    
def CheckVittoria(gameboard):
    cv = [
        ("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9"),
        ("1", "4", "7"), ("2", "5", "8"), ("3", "6", "9"),
        ("1", "5", "9"), ("3", "5", "7")        
    ]
    for c in cv:
        if gameboard[c[0]] == gameboard[c[1]] == gameboard[c[2]] != None:
            print(f"Vittoria per {gameboard[c[0]]}")
            return True
    return False

def StampaMatrice(gameboard):
    system('cls')
    for j in range (1, 8, 3):
        print(f"{gameboard[str(j)]}\t{gameboard[str(j+1)]}\t{gameboard[str(j+2)]}")

win = False
for z in range(9):
    StampaMatrice(gameboard)
    print(i)
    if(i == 0):
        
        FillMatrix()
        i = 1
    else:
        stringedGameboard = str(gameboard)
        azioni_disponibili = azioni_disponibili_da_stringa(str(stringedGameboard))
        azione = scegli_azione(str(stringedGameboard), azioni_disponibili, Q_tableO)
        gameboard = esegui_mossa(gameboard, azione, 'O')
        i = 0
    win = CheckVittoria(gameboard)
    if win :
        StampaMatrice(gameboard)
        winner = "X" if i == 1 else "O"
        if(winner == "X"):
            aggiorna_q_table(stringedGameboard, azione, -2, str(gameboard), azioni_disponibili, 0.5, 1, Q_tableO)
            UpdateTableFile()
        print(f"Vince il giocatore {winner}")
        break
if not win:
    print("Pareggio")

