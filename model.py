import json
import random
import os
import trisNoGUI #a me da errore di importazione ma chiama comunque le funzioni, boh ~Cristian
                 #comunque doveva servire da versione NOGUI ma alla fine richiama solo qualche funzione che potrei passare a questo file

Q_tableX = {}  # Chiave: stato (tupla (dict, azione)), valore)
Q_tableO = {} 
alpha = 0.5 #valori per l'allenamento del modello, globali perché almeno non va né passato né ritornato nelle funzioni
gamma = 0.9
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

j = 0


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

def scegli_azione(stato, azioni_disponibili, Q_table, epsilon=0.1):
    if random.random() < epsilon:  # Esplorazione
        return random.choice(azioni_disponibili)
    else:  # Sfruttamento
        q_values = Q_table.get(stato, {})
        if q_values:  # Se ci sono valori Q noti per questo stato
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
    for _ in range(num_partite):
        gameboard = trisNoGUI.Reset()  # Resetta il tabellone, e il contatore dei turni
        lastPlayed = random.randint(0, 1)
        global alpha 
        alpha = 0.6
        global gamma 
        gamma = 1
        fine_partita = False
        stato_corrente = gameboard
        ricompensa = 0
        while not fine_partita:
                azioni_disponibili = azioni_disponibili_da_stringa(str(stato_corrente))
                currState = str(stato_corrente)
                if(lastPlayed == 0):
                    azione = scegli_azione(str(stato_corrente), azioni_disponibili, Q_tableX)
                    nuovo_stato = esegui_mossa(stato_corrente, azione, 'X')
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                else:
                    azione = scegli_azione(str(stato_corrente), azioni_disponibili, Q_tableO)
                    nuovo_stato = esegui_mossa(stato_corrente, azione, 'O')
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                trisNoGUI.StampaMatrice(nuovo_stato)
                fine_partita = trisNoGUI.CheckVittoria(nuovo_stato)
                print(f"Azioni disponibili: {azioni_disponibili_da_stringa(str(nuovo_stato))}") 
                if (fine_partita):
                    ricompensa = 100
                    if(lastPlayed == 1):
                        aggiorna_q_table(currState, azione, -2, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                        aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                    else:
                        aggiorna_q_table(currState, azione, -2, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                        aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                else:
                    ricompensa = 0.1
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                if None not in nuovo_stato.values() and not fine_partita:
                    print("Pareggio")
                    ricompensa = 1
                    fine_partita = True
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableX)
                    aggiorna_q_table(currState, azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma, Q_tableO)
                stato_corrente = nuovo_stato
                if fine_partita:
                    break
                if(lastPlayed == 0):
                    lastPlayed = 1
                else:
                    lastPlayed = 0
        print(f"Partite mancanti: {100000 - _}")
            
    #            for giocatore in ['X', 'O']:
    #            azioni_disponibili = azioni_disponibili_da_stringa(str(stato_corrente))
    #            azione = scegli_azione(str(stato_corrente), azioni_disponibili)
    #            nuovo_stato = esegui_mossa(stato_corrente, azione, giocatore)   #un sacco di variabili inutili ma almeno è leggibile
    #            trisNoGUI.StampaMatrice(nuovo_stato)
    #            fine_partita = trisNoGUI.CheckVittoria(nuovo_stato)
    #            print(f"Azioni disponibili: {azioni_disponibili_da_stringa(str(nuovo_stato))}") #creo una nuova variabile perché se no dovrei sovrascrivere azioni disponibili
    #            ricompensa = 0                                                                  #e non si può altrimenti ciao ciao aggiornamento della Qtable
    #            if (fine_partita):
    #                ricompensa += 1 - j
    #            else:
    #                ricompensa += 1
    #            if None not in nuovo_stato.values():
    #                print("Pareggio")
    #                ricompensa /= 2
    #                fine_partita = True
    #            aggiorna_q_table(str(stato_corrente), azione, ricompensa, str(nuovo_stato), azioni_disponibili, alpha, gamma )
    #            stato_corrente = nuovo_stato
    #            if fine_partita:
    #                break
                    
'''
allenamento(100000)
with open('qtablex.txt', 'w') as file:
    for key, value in Q_tableX.items():
        file.write(f'{key}:{value}\n')
with open('qtableo.txt', 'w') as file:
    for key, value in Q_tableO.items():
        file.write(f'{key}:{value}\n')
'''
