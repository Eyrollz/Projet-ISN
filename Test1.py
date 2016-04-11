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
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))#,FULLSCREEN)
#On ouvre le niveau.lvl et on lit ce qui y est écrit
monLvl = open("Ressources/monNiv.lvl", "r")
contenu = monLvl.read()
monLvl.close()

dessinerSbire = False
grdeMap = pygame.image.load("Ressources/Sprites_Env.png")
menu_1 = pygame.image.load("Ressources/Menu_1.png")
tourelles_E =  pygame.image.load("Ressources/tourelles.png")

tourelle_1 = tourelles_E.subsurface(0,0,32,53)
tourelle_2 = tourelles_E.subsurface(127,0,18,32)
tourelle_3 = tourelles_E.subsurface(197,0,31,43)
tourelle_1m = tourelle_1.convert()
tourelle_2m = tourelle_2.convert()
tourelle_3m = tourelle_3.convert()
pos_menu_1_X = -1
pos_menu_1_Y = -1

tourelle_2m.set_alpha(150)

sbire_1_E = pygame.image.load("Ressources/sbire_1.png")
sbire_1 = sbire_1_E.subsurface(0,0,32,32)

#print(contenu)

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



#Variable qui continue la boucle si = 1, stoppe si = 0

continuer = 1
pygame.display.flip()

#Boucle infinie
while continuer:
   
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos_menu_1_X = event.pos[0]
            pos_menu_1_Y = event.pos[1]

        if event.type == QUIT:
            continuer = 0
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                continuer = 0
                pygame.quit()

    for i in range (0,32):
        for j in range (0,25):
            fenetre.blit(Carte[j][i], (i*LARGEUR_CASE,j*HAUTEUR_CASE))
        if event.type == KEYUP:
            dessinerSbire = True

    if dessinerSbire == True:
        fenetre.blit(sbire_1,(0,0))

    if pos_menu_1_X != -1 and pos_menu_1_Y !=-1 :
        fenetre.blit(menu_1,(pos_menu_1_X,pos_menu_1_Y))
        (w1,h1) = tourelle_2.get_size()
        (w2,h2) = tourelle_3.get_size()
        print(" w1 w2",w1, "  ",w2)
        fenetre.blit(tourelle_1m,(pos_menu_1_X+14,pos_menu_1_Y+14))
        fenetre.blit(tourelle_2m,(pos_menu_1_X+14+w2,pos_menu_1_Y+14))
        fenetre.blit(tourelle_3m,(pos_menu_1_X+14+w2+w1,pos_menu_1_Y+14))

    #Rafraichissement
    pygame.display.flip()

            
    continue #Je place continue ici pour pouvoir relancer la boucle infinie
                 #mais il est d'habitude remplacé par une suite d'instructions
