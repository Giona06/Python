import json
import random
import os
import trisNoGUI #a me da errore di importazione ma chiama comunque le funzioni, boh ~Cristian
from threading import Thread, Lock   #comunque doveva servire da versione NOGUI ma alla fine richiama solo qualche funzione che potrei passare a questo file

Q_tableX = {}  # Chiave: stato (tupla (dict, azione)), valore)
Q_tableO = {} 
alpha = 0.60 #valori per l'allenamento del modello, globali perché almeno non va né passato né ritornato nelle funzioni
gamma = 0.90
if os.path.exists('qtablex.text'):
    with open('qtablex.txt', 'r') as file:
        input_string = file.readline()
        # Separazione della stringa del dizionario e del float
        dict_string, float_string = input_string.split('):')
        # Rimozione delle parentesi dalla stringa del dizionario
        dict_string = dict_string[1:]
        # Creazione del dict con il dizionario convertito e il float
        Q_tableX[eval(dict_string)] = float(float_string)
else:
    Q_tableX = {}
if os.path.exists('qtableo.text'):
    with open('qtableo.txt', 'r') as file:
        input_string = file.readline()
        # Separazione della stringa del dizionario e del float
        dict_string, float_string = input_string.split('):')
        # Rimozione delle parentesi dalla stringa del dizionario
        dict_string = dict_string[1:]
        # Creazione del dict con il dizionario convertito e il float
        Q_tableO[eval(dict_string)] = float(float_string)
else:
    Q_tableO = {}

def azioni_disponibili_da_stringa(gameboard_str):
    """
    Prende come input una stringa che rappresenta un dizionario di gameboard e
    restituisce una lista dei numeri dei quadranti disponibili (come interi).
    """
    #passare da dict a stringa è atroce ma funziona, non voglio rischiare modificandolo
    # Converti la stringa in un dizionario
    gameboard_str = gameboard_str.replace("'", '"')
    gameboard_str = gameboard_str.replace("None", '""')
    gameboard = json.loads(gameboard_str)
    
    # Trova le posizioni disponibili
    return [posizione for posizione, valore in gameboard.items() if valore == ""]


def esegui_mossa(gameboard, posizione, simbolo):
    """
    Esegue una mossa nel gioco del tris, aggiornando il gameboard con il simbolo del giocatore nella posizione scelta.

    Args:
        gameboard (dict): Il dizionario che rappresenta lo stato corrente del gioco.
        posizione (str): La chiave nel dizionario che indica la posizione scelta per la mossa.
        simbolo (str): Il simbolo del giocatore che esegue la mossa, "X" o "O".

    Returns:
        dict: Il gameboard aggiornato dopo aver eseguito la mossa.
    """
    
    gameboard[posizione] = simbolo

    return gameboard

def scegli_azione(stato, azioni_disponibili, Q_table, epsilon):
    if random.random() < 0.2 - epsilon:  # Esplorazione
        return random.choice(azioni_disponibili)
    else:  # Sfruttamento
        q_values = Q_table.get(stato, {})
        if q_values:  # Se ci sono valori Q noti per questo stato
            if(max(q_values, key=q_values.get) < 0):
                return random.choice(azioni_disponibili)
            else:
                return max(q_values, key=q_values.get)  # Scegli la mossa con il massimo valore Q
        return random.choice(azioni_disponibili)  # Caso in cui non ci sono mosse conosciute

def aggiorna_q_table(stato, azione, ricompensa, stato_successivo, azioni_disponibili, alpha, gamma, Q_table):
    
    q_attuale = Q_table.get((stato, azione), 0)  # Ottiene il valore Q corrente, 0 se non esistente
    q_massimo_futuro = max(Q_table.get((stato_successivo, a), 0.1) for a in azioni_disponibili)
    q_target = ricompensa + gamma * q_massimo_futuro  # Calcola il target Q
    Q_table[(stato, azione)] = q_attuale + alpha * (q_target - q_attuale)  # Aggiorna il valore Q nella tabella
    #alpha += 0.05

def allenamento(num_partite):
    #TODO creare una funzione che calcoli effettivamente la ricompensa per scelte intelligenti come il continuo di una streak o interrompere quella di un altro
    global Q_tableX
    global Q_tableO
    j = 0
    for _ in range(num_partite):
        os.system('cls')
        gameboard = trisNoGUI.Reset()  # Resetta il tabellone, e il contatore dei turni
        lastPlayed = random.randint(0, 1) #Sceglie a caso quale giocatore comincia
        fine_partita = False
        stato_corrente = gameboard
        ricompensa = 0
        azioneX = ''
        azioneO = ''
        j = 0
        while not fine_partita:
            azioni_disponibili = azioni_disponibili_da_stringa(str(stato_corrente))
            currState = str(stato_corrente)
            if(lastPlayed == 0):
                azioneX = scegli_azione(str(stato_corrente), azioni_disponibili, Q_tableX, j/50)
                nuovo_stato = esegui_mossa(stato_corrente, azioneX, 'X')
            else:
                azioneO = scegli_azione(str(stato_corrente), azioni_disponibili, Q_tableO, j/50)
                nuovo_stato = esegui_mossa(stato_corrente, azioneO, 'O')
            fine_partita = trisNoGUI.CheckVittoria(nuovo_stato)
            #print(f"Azioni disponibili: {azioni_disponibili_da_stringa(str(nuovo_stato))}\n") 
            if (fine_partita):
                ricompensa = 19 - j
                if(lastPlayed == 1):
                    aggiorna_q_table(statoPrecedente, azionePrecedenteX, -(10 + (10 - j/2)), str(currState), azioni_disponibiliPrecedenti, alpha, gamma, Q_tableX)
                    aggiorna_q_table(currState, azioneO, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                else:
                    aggiorna_q_table(statoPrecedente, azionePrecedenteO, -(10 + (10 - j/2)), str(currState), azioni_disponibiliPrecedenti, alpha, gamma, Q_tableO)
                    aggiorna_q_table(currState, azioneX, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
            else:
                ricompensa = 0.01 + j/100
                if(lastPlayed == 1):
                    aggiorna_q_table(currState, azioneO, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                else:
                    aggiorna_q_table(currState, azioneX, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
            if None not in nuovo_stato.values() and not fine_partita:
                print("Pareggio")
                ricompensa = 2
                if(lastPlayed == 1):
                    aggiorna_q_table(currState, azioneO, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                    aggiorna_q_table(statoPrecedente, azionePrecedenteX, ricompensa, str(currState), azioni_disponibiliPrecedenti, alpha, gamma, Q_tableX)
                else:
                    aggiorna_q_table(currState, azioneX, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                    aggiorna_q_table(statoPrecedente, azionePrecedenteO, ricompensa, str(currState), azioni_disponibiliPrecedenti, alpha, gamma, Q_tableO)
                fine_partita = True
            stato_corrente = nuovo_stato
            azionePrecedenteX = azioneX
            azionePrecedenteO = azioneO
            statoPrecedente = currState
            azioni_disponibiliPrecedenti = azioni_disponibili
            if(lastPlayed == 0):
                lastPlayed = 1
            else:
                lastPlayed = 0
            j += 1
        print(f"Partite mancanti: {1000000 - _}")
    blocco.acquire()
    tableXcopy = Q_tableX.copy()
    tableOcopy = Q_tableO.copy()
    with open('qtablex.txt', 'w') as file:
        for key, value in tableXcopy.items():
            file.write(f'{key}:{value}\n')
    with open('qtableo.txt', 'w') as file:
        for key, value in tableOcopy.items():
            file.write(f'{key}:{value}\n')
    blocco.release()

blocco = Lock()

class Train (Thread):
    def __init__(self, nome):
        Thread.__init__(self)
        self.nome = nome
    def run(self):
        allenamento(1000000)


thread1 = Train("Thread1")
thread2 = Train("Thread2")
thread3 = Train("Thread3")
thread4 = Train("Thread4")
thread5 = Train("Thread5")
thread6 = Train("Thread6")
thread7 = Train("Thread7")
thread8 = Train("Thread8")
thread9 = Train("Thread9")
thread0 = Train("Thread0")

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread0.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread0.join()