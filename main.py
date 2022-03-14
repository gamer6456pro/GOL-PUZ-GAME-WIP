from ast import Pass
import math
import copy
import pygame 
import sys
from pygame.locals import *
from pygame import cursors
pygame.init()
FPS=pygame.time.Clock()
font=pygame.font.Font('C:/Users/Austin/Programming/Pygame/Fonts/RetniSans-Medium.ttf',35)
LEVELCOMPLETETXT=font.render("You beat level 1",False,(81,118,252))# -----> use arg and tell the player to move on the next level somewho 
GREEN=pygame.Color(0,255,0)
WHITE=pygame.Color(255,255,255)
YELLOW=pygame.Color(255,255,0)
BLACK=pygame.Color(0,0,0)
RED=pygame.Color(255,0,0)
window=pygame.display.set_mode((1200,800))
GOLSurface=pygame.Surface((800,800))
pygame.display.set_caption("GOL Puz Game")
BUTTONS=pygame.image.load("C:/Users/Austin/Programming/Pygame/GOL Puz Game/images/buttons.png")
gameState='placeMode' 

'''startscreen=menu
simulation=running GOL
placeMode=using mouse to place
settings=screen to change simulation speed and some future things too
levelComplete=the win screen with buttons to go to next level, menu, and start screen
pause=simulation is stopped'''


class levels():
    def __init__(self, array, arrayPlaceArea, objectiveCoords):# -----> have array place area be like 2 constants and then multiply by 100 and check if in bound when clickign 
        self.array=array
        self.arrayPlaceArea=arrayPlaceArea
        self.objectiveCoords=objectiveCoords

def createGrid(x,y):
    outPutGrid=[]
    for i in range(x):
        row=[]
        outPutGrid.append(row)
        for j in range(y):
            row.append(False)
    return outPutGrid

def lvl1(): # -----> maybe put this into the class 
    lvl1Grid=createGrid(8,8)
    lvl1ArrayPlaceArea=createGrid(3,3)
    lvl1=levels(lvl1Grid,lvl1ArrayPlaceArea,[5,5]) 
    return lvl1

def generateGen(lvlArrayObj):
    NewGen=copy.deepcopy(lvlArrayObj)
    aliveNeighbors=0
    for i,x in enumerate(lvlArrayObj):
        for j,y in enumerate(x):
            aliveNeighbors=0
            # -----> change this with dimesions of grid so use arg but idk like the less than 8 stuff
            if i-1>-1 and j-1>-1:
                if lvlArrayObj[i-1][j-1]:
                    aliveNeighbors+=1
            if i-1>-1:
                if lvlArrayObj[i-1][j]:
                    aliveNeighbors+=1
            if i-1>-1 and j+1<8:
                if lvlArrayObj[i-1][j+1]:
                    aliveNeighbors+=1
            if j-1>-1:
                if lvlArrayObj[i][j-1]:
                    aliveNeighbors+=1
            if j+1<8:
                if lvlArrayObj[i][j+1]:
                    aliveNeighbors+=1
            if i+1<8 and j-1>-1:
                if lvlArrayObj[i+1][j-1]:
                    aliveNeighbors+=1
            if i+1<8:
                if lvlArrayObj[i+1][j]:
                    aliveNeighbors+=1
            if i+1<8 and j+1<8:
                if lvlArrayObj[i+1][j+1]:
                    aliveNeighbors+=1
            if aliveNeighbors<2:
                NewGen[i][j]=False
            elif (aliveNeighbors==2 or aliveNeighbors==3) and NewGen[i][j]:
                NewGen[i][j]=True
            elif aliveNeighbors>3:
                NewGen[i][j]=False
            elif aliveNeighbors==3:
                NewGen[i][j]=True
    return NewGen   

def simulation():
    global newGen
    global pastGen
    newGen=generateGen(pastGen)
    pastGen=copy.deepcopy(newGen)
    pygame.time.wait(242)# -----> this can be adjusted

def drawGeneration(newGen):
    for i,x in enumerate(newGen):
        for j,_ in enumerate(x):
            if newGen[i][j]:
                pygame.draw.rect(GOLSurface,GREEN,(j*100+2,2+i*100,97,97))

def drawGrid():
    GOLSurface.fill((0,0,0))
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(GOLSurface,WHITE,(i*100,j*100,100,100),1)
    for i,x in enumerate(lvl1.arrayPlaceArea):
        for j,y in enumerate(x):
            pygame.draw.rect(GOLSurface,YELLOW,((len(x)-1+i)*100,(len(x)-1+j)*100,101,101),3)
    pygame.draw.rect(GOLSurface, RED,(lvl1.objectiveCoords[0]*100-1,lvl1.objectiveCoords[1]*100-1,101,101),3)

lvl1=lvl1()
newGen=[]
pastGen=[]
window.fill((0,0,0))
window.blit(BUTTONS,(800,0))
mouseClicked=False
while True:
    

    drawGrid()
    for event in pygame.event.get(): # -----> set past gen to equal the current array when the player clicks start simulation in the mousedown section 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouseClicked=True
                mouseX, mouseY=pygame.mouse.get_pos()
                mouseXIndex=math.floor(mouseX/100)
                mouseYIndex=math.floor(mouseY/100)
                if gameState=='placeMode' and 1<mouseXIndex<5 and 1<mouseYIndex<5:# -----> same thing here prob make into func with args 
                    # -----> This is hardcoded 
                    lvl1.array[mouseYIndex][mouseXIndex]= not lvl1.array[mouseYIndex][mouseXIndex] # -----> make this somehow use the specific level input 
                    
                elif 800<mouseX<941 and 0<mouseY<105:
                    pastGen=copy.deepcopy(lvl1.array)  

                    gameState='simulation'
                    simulation()
                elif 618<mouseX<1200 and 0<mouseY<107:
                    if gameState=='pause':
                        gameState='simulation' # -----> can make this one button 
                    else:
                        gameState='pause'
                elif 800<mouseX<940 and 133<mouseY<231:
                    gameState='restart'

                    
    if gameState=='simulation' and newGen[lvl1.objectiveCoords[0]][lvl1.objectiveCoords[1]]: # -----> no need for level Complete but im keeping it for organization maybe 
        gameState='levelComplete'
    if gameState=='levelComplete':
        window.blit(LEVELCOMPLETETXT,(850,350))
        drawGeneration(newGen)

    if gameState=='restart':
        gameState='placeMode' # -----> change this to maybe elif 
    if gameState=='pause':
        continue
    if gameState=='startScreen':
        pass # -----> currently prob not going to make 
    if gameState=='simulation':
        drawGeneration(newGen)
        simulation()
    window.blit(GOLSurface,(0,0))# -----> this prob clears the placing ting so maybe put insdie gameState==simulation 
    if gameState=='placeMode' and mouseClicked:
        for i,x in enumerate(lvl1.array): # -----> use corrrect level somehow make func prob 
            for j,_ in enumerate(x):
                if lvl1.array[i][j]:
                    pygame.draw.rect(window,GREEN, (j*100+2,2+100*i,97,97))
   
    pygame.display.update()
    FPS.tick(60)
    
