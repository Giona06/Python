from os import system
gameboard = {
        "1" : None, "2" :None, "3" : None,
        "4" : None, "5" : None, "6" : None,
        "7" : None, "8" : None, "9" : None
    }
i = 0
playerChar = lambda i : "X" if i % 2 == 0 else "O"
def Reset():
    global gameboard
    gameboard = {
        "1" : None, "2" :None, "3" : None,
        "4" : None, "5" : None, "6" : None,
        "7" : None, "8" : None, "9" : None
    }
    global i 
    i= 0
    return gameboard

"""def FillMatrix():
    global i
    i += 1
    foundValidPosition = False
    while not foundValidPosition:

        if gameboard[n] is None:
            gameboard[n] = playerChar(i)
            foundValidPosition = True
        else:
            foundValidPosition = False
    """
    
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
"""
win = False
for z in range(9):
    StampaMatrice(gameboard)
    #FillMatrix()
    win = CheckVittoria(gameboard)
    if win :
        StampaMatrice(gameboard)
        print(f"Vince il giocatore {playerChar(i)}")
        break
if not win:
    print("Pareggio")
"""