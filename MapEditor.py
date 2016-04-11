#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *

#Faire une map de meme taille que celle de base
# mais avec tile 16x16
#Initialisation de la bibliothèque Pygame
pygame.init()
#Initialisation des variables utiles
LARGEUR_CASE =32
HAUTEUR_CASE= 32
LARGEUR_FENETRE = 32* 32
HAUTEUR_FENETRE = 25 * 32

directionFleche = "droite"
#On ouvre le niveau.lvl et on lit ce qui y est écrit
monLvl_Col = open("Ressources/Map_Path.lvl", "w")

monLvl_Col.close()

monLvl = open("Ressources/monNiv.lvl", "r")
contenu = monLvl.read()
monLvl.close()

dessinerSbire = False

fleches_E = pygame.image.load("Ressources/fleche_dir.png")
grdeMap = pygame.image.load("Ressources/Sprites_Env.png")

sbire_1_E = pygame.image.load("Ressources/sbire_1.png")
sbire_1 = sbire_1_E.subsurface(0,0,32,32)

posSourisX = -1
posSourisY = -1

lvl = contenu.split()

Map = [[0] * 28 for _ in range(61)]
Carte = [[0] * 32 for _ in range(25)]

x=0

for i in range (0,61):
    for j in range (0,28):

        Map[i][j]= grdeMap.subsurface(i*16+i,j*16+j,16,16)
        Map[i][j]= pygame.transform.scale(Map[i][j],(LARGEUR_CASE,HAUTEUR_CASE))

for i in range (0,25):
    for j in range (0,32):
        mapY=int(int(lvl[x])/61)
        Carte[i][j]= Map[int(int(lvl[x])-(mapY*61))][mapY]
        #print("x : ",x,"\n")
        x=x+1

#Création de la fenêtre

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))#,FULLSCREEN)

#Variable qui continue la boucle si = 1, stoppe si = 0

continuer = 1
pygame.display.flip()

#Boucle infinie
while continuer:


    if directionFleche == "droite":
        print("d")
        fleches = fleches_E.subsurface(0,0,32,32)
    if directionFleche == "bas":
        print("b")
        fleches = fleches_E.subsurface(32,0,32,32)
    if directionFleche == "gauche":
        print("g")
        fleches = fleches_E.subsurface(64,0,32,32)
    if directionFleche == "haut":
        print("h")
        fleches = fleches_E.subsurface(96,0,32,32)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1:# and event.pos[1] < 100:
            print("Zone dangereuse X : ",int(event.pos[0]/32)," Y :",int(event.pos[1]/32))
            posSourisX = int(event.pos[0]/32)
            posSourisY = int(event.pos[1]/32)
        if event.type == QUIT:
            continuer = 0
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                continuer = 0
                pygame.quit()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                directionFleche= "droite"
            if event.key == K_DOWN:
                directionFleche= "bas"
            if event.key == K_LEFT:
                directionFleche= "gauche"
            if event.key == K_UP:
                directionFleche= "haut"
            dessinerSbire = True
    if dessinerSbire == True:
        fenetre.blit(sbire_1,(0,0))

    for i in range (0,32):
        for j in range (0,25):
            fenetre.blit(Carte[j][i], (i*LARGEUR_CASE,j*HAUTEUR_CASE))
    if posSourisX != -1 and posSourisY != -1 :
        fenetre.blit(fleches,(posSourisX*32,posSourisY*32))$


    #Rafraichissement
    pygame.display.flip()


    continue #Je place continue ici pour pouvoir relancer la boucle infinie
                 #mais il est d'habitude remplacé par une suite d'instructions
