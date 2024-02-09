import turtle
import time

gameboard = {
    "1" : None, "2" :None, "3" : None,
    "4" : None, "5" : None, "6" : None,
    "7" : None, "8" : None, "9" : None
}
def ClickedCoord(x, y):
    print(x)
    print(y)
squareCoords = {
    "1" : (-320, 320), "2" : (-105, 320), "3" : (110, 320),
    "4" : (-320, 105), "5" : (-105, 105), "6" : (110, 105),
    "7" : (-320, -110), "8" : (-105, -110), "9" : (110, -110)
    }
def FillMatrix(x,y):
    global i
    i += 1
    for c in squareCoords:
        if( squareCoords[c][0] < x < (squareCoords[c][0]+ 210) and squareCoords[c][1] > y > (squareCoords[c][1] - 210)):
            if(gameboard[c] == None):
                gameboard[c] = playerChar(i)
                DisegnaSimbolo(c)
            else:
                i-=1
    vittoria = CheckVittoria()
    if vittoria[3]:
        Strike(vittoria)
    if i == 9 or vittoria[3]:
        print(f"Vince il giocatore {gameboard[vittoria[1]]}")
        time.sleep(7)
        turtle.bye()

def CheckVittoria():
    cv = [
        ("1", "2", "3"), ("4", "5", "6"), ("7", "8", "9"),
        ("1", "4", "7"), ("2", "5", "8"), ("3", "6", "9"),
        ("1", "5", "9"), ("3", "5", "7")        
    ]
    for c in cv:
        if gameboard[c[0]] == gameboard[c[1]] == gameboard[c[2]] != None:
            return (c[0], c[1], c[2], True)
    return (None, None, None, False)
def Strike(c):
    penna.penup()
    penna.color("green")
    if(c[0] == "1" and c[2] == "9"):
        penna.goto(squareCoords["1"][0], squareCoords["1"][1])
        penna.pendown()
        penna.goto(squareCoords["9"][0]+210, squareCoords["9"][1]-210)
    elif(c[0] == "3" and c[2] == "7"):
        penna.goto(squareCoords["7"][0], squareCoords["7"][1]-210)
        penna.pendown()
        penna.goto(squareCoords["3"][0]+210, squareCoords["3"][1])
    elif(int(c[0])+6 == int(c[2])):
        penna.goto(squareCoords[c[0]][0]+105, squareCoords[c[0]][1])
        penna.pendown()
        penna.goto(squareCoords[c[2]][0]+105, squareCoords[c[2]][1]-210)
    else:
        penna.goto(squareCoords[c[0]][0], squareCoords[c[0]][1]-105)
        penna.pendown()
        penna.goto(squareCoords[c[2]][0]+210, squareCoords[c[2]][1]-105)


def DisegnaSimbolo(c):
    penna.penup()
    penna.goto(squareCoords[c][0] + 105, squareCoords[c][1] - 105)
    if(gameboard[c] == "O"):
        penna.color('red')
        penna.goto(penna.pos()[0], penna.pos()[1] - 90)
        penna.pendown()
        penna.circle(90)
        penna.penup()
    else:
        penna.color('blue')
        penna.goto(penna.pos()[0] - 90, penna.pos()[1] + 90)
        penna.pendown()
        penna.goto(penna.pos()[0] + 180, penna.pos()[1] - 180)
        penna.penup()
        penna.goto(penna.pos()[0], penna.pos()[1] + 180)
        penna.pendown()
        penna.goto(penna.pos()[0] - 180, penna.pos()[1] - 180)
        penna.penup()
    penna.color('black')



def DisegnaCampo():

    penna.hideturtle()
    penna.penup()
    penna.color("black")
    penna.pensize(5)
    penna.goto(108,317)
    penna.pendown()
    penna.goto(108, -317)
    penna.penup()
    penna.goto(-108, -317)
    penna.pendown()
    penna.goto(-108, 317)
    penna.penup()
    penna.goto(317, 108)
    penna.pendown()
    penna.goto(-317, 108)
    penna.penup()
    penna.goto(-317, -108)
    penna.pendown()
    penna.goto(317, -108)
    penna.penup()


# Imposta la finestra
finestra = turtle.Screen()  # Crea una finestra per turtle
finestra.title("Tris")  # Imposta il titolo della finestra
finestra.bgcolor("white")  # Imposta il colore di sfondo della finestra
finestra.setup(width=640, height=640)  # Imposta le dimensioni della finestra

penna = turtle.Turtle()  # Crea un oggetto turtle per disegnare
penna.speed(0)  # Imposta la velocità di disegno al massimo
# Assegna la funzione di callback per gestire gli eventi di clic del mouse
DisegnaCampo()
i = 0
playerChar = lambda i : "X" if i % 2 == 0 else "O"
finestra.onclick(FillMatrix)
turtle.mainloop()



