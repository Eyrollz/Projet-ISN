#Importation des bibliothèques nécessaires
import GestionTourelles
import pygame
import math
from pygame.locals import *
#Modifier viteese et gérer range tourelles + tires img
#Finir les spawn de groupes de sbires
#Initialisation de la bibliothèque Pygame
pygame.init()

sbireEntier = pygame.image.load("Ressources/sbire_1.png")

sbireDroite1 =sbireEntier.subsurface(0 *32,2*32,32,32)
sbireHaut1 =sbireEntier.subsurface(0 *32,3*32,32,32)
sbireBas1 =sbireEntier.subsurface(0 *32,0*32,32,32)

sbireDroite2 =sbireEntier.subsurface(2 *32,2*32,32,32)
sbireHaut2 =sbireEntier.subsurface(2 *32,3*32,32,32)
sbireBas2 = sbireEntier.subsurface(2 *32,0*32,32,32)


sbireBase = sbireDroite1
# Création de la classe Sbire
class Sbire:
    global sbireDroite1
    global sbireHaut1
    global sbireBas1
    global sbireDroite2
    global sbireHaut2
    global sbireBas2
    def __init__(self): # Notre méthode constructeur

        self.posX = 0-32
        self.posY = 12*32
        self.direction = 6
        self.img = sbireDroite1
        self.spawn = False

#Initialisation des variables utiles
LARGEUR_CASE =32
HAUTEUR_CASE= 32
LARGEUR_FENETRE = 32* 32
HAUTEUR_FENETRE = 25 * 32
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))#,FULLSCREEN)
#On ouvre le ficher contenant les informations sur les collisions
collisions_fichier = open("Ressources/collisions.lvl", "r")
collisions_text = collisions_fichier.read()
collisions_fichier.close()
collisions = collisions_text.split()
collisions_liste=[[0] * 32 for _ in range(25)]

chemin_fichier = open("Ressources/chemin.lvl", "r")
chemin_text = chemin_fichier.read()
chemin_fichier.close()
chemin = chemin_text.split()
chemin_liste=[[0] * 32 for _ in range(25)]

posXSbire =0-32
posYSbire = 12*32


# Direction du sbire :
# Droite : 6
# Gauche : 4
# Bas : 5
# Haut : 8
directionSbire = 6

clock = pygame.time.Clock()

#On navigue dans la liste contenant les valeurs "0000" ou "0001" puis on crée un nouveau
# tableau 2D d'entiers avec '0' ou '1'
# 0 : On peut poser une tourelle
# 1 : On ne peut pas poser de tourelle
y_col=0
x_col=0
inc=0
for i in range (0,25):
    for j in range (0,32):
        if collisions[inc] == "0000":
            collisions_liste[i][j]= 0
        elif collisions[inc] == "0001":
            collisions_liste[i][j]= 1
        #print("x : ",x,"\n")
        inc=inc+1

y_col=0
x_col=0
inc=0
for i in range (0,25):
    for j in range (0,32):
        if chemin[inc] == "4":
            chemin_liste[i][j]= 4
        elif chemin[inc] == "5":
            chemin_liste[i][j]= 5
        elif chemin[inc] == "6":
            chemin_liste[i][j]= 6
        elif chemin[inc] == "8":
            chemin_liste[i][j]= 8
       
        
        inc=inc+1
print( "chemin : ",chemin_liste)




#On ouvre le niveau.lvl et on lit ce qui y est écrit
monLvl = open("Ressources/monNiv.lvl", "r")
contenu = monLvl.read()
monLvl.close()
lvl = contenu.split()

# Numéro de la tourelle séléctionée ( dans le menu )
choixMenu = 0
menuOuvert = False


grdeMap = pygame.image.load("Ressources/Sprites_Env.png")
menu_1 = pygame.image.load("Ressources/Menu_1.png")
tourelles_E =  pygame.image.load("Ressources/tourelles.png")

# On charge l'image des sbores



# On découpe l'image pour avoir les différentes tourelles
tourelle_1 = tourelles_E.subsurface(42,0,53,31)
tourelle_2 = tourelles_E.subsurface(258,0,32,30)
tourelle_3 = tourelles_E.subsurface(0,0,43,31)

# Création des tourelles du menu ( afin de pouvoir utiliser la transparence)
tourelle_1m = tourelle_1.convert()
tourelle_2m = tourelle_2.convert()
tourelle_3m = tourelle_3.convert()

#Tableau de tourelles et de leurs attributs :
tabTourelles = []
tabTourelles_Pos_X = []
tabTourelles_Pos_Y = []
typeTourelle = []

#Position du menu
pos_menu_1_X = -1
pos_menu_1_Y = -1


nbMaxTourMenu = 3-1
dessinTour = False

# Intervalle de temps entre 2 apparitions
# de 1000 milisec, soit 1 seconde
deltaTSpawn = 0

numManche = 1
nbSbiresMax = 3
nbSbireAct=0
vitesseSbires = 150

# Création de la liste des sbires :
sbiresManches = []





def DebutManche():
    global deltaTSpawn
    global sbiresManches
    global nbSbiresMax
    global nbSbireAct
    tps = pygame.time.get_ticks()     #temps
    tps2 = temps - deltaTSpawn

    if (tps2 - 1000 > 0) and nbSbireAct < nbSbiresMax:      # Chaque 500 ms le sbire se déplace

        deltaTSpawn += 1000
        tps2 = tps2 - deltaTSpawn
        sbireTemp = Sbire()
        sbiresManches.append(sbireTemp)
        nbSbireAct +=1

def DessinerTourelles():
    global dessinTour
    if menuOuvert:

        #Si le menu est ouvert on dessine les différentes tourelles dedans
        #selon celle qui est choisie
        fenetre.blit(menu_1,(pos_menu_1_X,pos_menu_1_Y))
        # On change la transparence des icones du menu
        # selon la tourelle séléctionnée
        if choixMenu == 0:
            tourelle_1m.set_alpha(255)
            tourelle_2m.set_alpha(100)
            tourelle_3m.set_alpha(100)
        if choixMenu == 1:
            tourelle_1m.set_alpha(100)
            tourelle_2m.set_alpha(255)
            tourelle_3m.set_alpha(100)
        if choixMenu == 2:
            tourelle_1m.set_alpha(100)
            tourelle_2m.set_alpha(100)
            tourelle_3m.set_alpha(255)

        (w1,h1) = tourelle_2.get_size()
        (w2,h2) = tourelle_3.get_size()

        fenetre.blit(tourelle_1m,(pos_menu_1_X+14,pos_menu_1_Y+14))
        fenetre.blit(tourelle_2m,(pos_menu_1_X+30+w2,pos_menu_1_Y+14))
        fenetre.blit(tourelle_3m,(pos_menu_1_X+40+w2+w1,pos_menu_1_Y+14))
    if dessinTour == True :
        print("Dessin des tourelles")
        if choixMenu == 0:
            tabTourelles.append(tourelle_1)
            typeTourelle.append(1)
        elif choixMenu == 1:
            tabTourelles.append(tourelle_2)
            typeTourelle.append(2)
        elif choixMenu == 2:
            tabTourelles.append(tourelle_3)
            typeTourelle.append(3)

       # tabTourelles.append(tourelle_1)
        tabTourelles_Pos_X.append(int(pos_menu_1_X/32)*32-15+16)
        tabTourelles_Pos_Y.append(int(pos_menu_1_Y/32)*32-37+16)
        dessinTour=False
    for i in range(len(tabTourelles)):
            fenetre.blit(tabTourelles[i],(tabTourelles_Pos_X[i],tabTourelles_Pos_Y[i]))
def BougerSbire( sbire):
    global posXSbire
    global posYSbire
    global direction
    global sbireBase
    global sbireGauche1
    global sbireBas1
    global sbireDroite1
    global sbireHaut1
    global sbireGauche2
    global sbireBas2
    global sbireDroite2
    global sbireHaut2
    nbDepl = 8
    changerImg= False

    print("direction : ",sbire.direction)
    print( " X : ",int(sbire.posX/32)," Y : ",int(sbire.posY/32))
    print(" chemin : ",chemin_liste[int((sbire.posY/32))][int((sbire.posX+32)/32)+1])

    tempX =sbire.posX
    tempY =sbire.posY


            
    if sbire.direction == 5:

        #print(" X: ",int(sbire.posX/32)," Y: ",int(sbire.posY/32))

        if chemin_liste[int((sbire.posY/32))+1][int((sbire.posX+32)/32)] == 5 :
            if(sbire.img != sbireBas2 and changerImg == False):
                sbire.img = sbireBas2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg=True
            elif(sbire.img != sbireBas1 and changerImg == False):
                sbire.img = sbireBas1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg == True
            sbire.posY = sbire.posY +nbDepl
            sbire.direction = 5
        if chemin_liste[int((sbire.posY/32))+1][int((sbire.posX+32)/32)] == 6 :
            if(sbire.img == sbireDroite1 and changerImg == False):
                sbire.img = sbireDroite2
                changerImg=True
            elif(sbire.img == sbireDroite2 and changerImg == False):
                sbire.img = sbireDroite1
                changerImg=True
            sbire.posX = sbire.posX +nbDepl
            sbire.direction = 6
        if chemin_liste[int((sbire.posY/32))+1][int((sbire.posX+32)/32)] == 8 :
            if(sbire.img != sbireHaut2 and changerImg == False):
                sbire.img = sbireHaut2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            elif(sbire.img != sbireHaut1 and changerImg == False):
                sbire.img = sbireHaut1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            sbire.posY = sbire.posY -nbDepl
            sbire.direction = 8
            
    if sbire.direction == 6:

        print("dans le 6")
        if chemin_liste[int(sbire.posY/32)][int((sbire.posX)/32)+1] == 5 :
            #print("euhhhhhhhhhhhhhhhhhhhh ???")
            if(sbire.img == sbireBas1 and changerImg == False):
                sbire.img = sbireBas2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg=True
            elif(sbire.img == sbireBas2 and changerImg == False):
                sbire.img = sbireBas1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            sbire.posY = sbire.posY +nbDepl
            sbire.direction = 5
        if chemin_liste[int((sbire.posY/32))][int((sbire.posX)/32)+1] == 6 :

            if(sbire.img != sbireDroite2 and changerImg == False):
                sbire.img = sbireDroite2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            elif(sbire.img != sbireDroite1 and changerImg == False):
                sbire.img = sbireDroite1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            sbire.posX = sbire.posX +nbDepl
            sbire.direction = 6
        if chemin_liste[int(sbire.posY/32)][int((sbire.posX)/32)+1] == 8 :
            if(sbire.img != sbireHaut2 and changerImg == False):
                sbire.img = sbireHaut2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            elif(sbire.img != sbireHaut1 and changerImg == False):
                sbire.img = sbireHaut1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True

            sbire.direction = 8
    if sbire.direction == 8:


        if chemin_liste[int((sbire.posY/32))-1][int((sbire.posX+32)/32)] == 5 :
            if(sbire.img == sbireBas1 and changerImg == False):
                sbire.img = sbireBas2
                changerImg=True
            elif(sbire.img == sbireBas2 and changerImg == False):
                sbire.img = sbireBas1
            sbire.posY = sbire.posY +nbDepl
            sbire.direction = 5
        if chemin_liste[int((sbire.posY/32))-1][int((sbire.posX+32)/32)] == 6 :
            if(sbire.img == sbireDroite1 and changerImg == False):
                sbire.img = sbireDroite2
                changerImg=True
            elif(sbire.img == sbireDroite2 and changerImg == False):
                sbire.img = sbireDroite1
                changerImg=True
            sbire.posY = sbire.posY -nbDepl
            sbire.posX = sbire.posX +nbDepl
            sbire.direction = 6
        if chemin_liste[int((sbire.posY/32))-1][int((sbire.posX+32)/32)] == 8 :

            if(sbire.img != sbireHaut2 and changerImg == False):
                sbire.img = sbireHaut2
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            elif(sbire.img != sbireHaut1 and changerImg == False):
                sbire.img = sbireHaut1
                sbire.posX = tempX
                sbire.posY = tempY
                changerImg= True
            sbire.posY = sbire.posY -nbDepl
            sbire.direction = 8
def PoserTourelle(event):
    # On utilise les variables global
    global menuOuvert
    global choixMenu
    global pos_menu_1_X
    global pos_menu_1_Y
    global dessinTour
    # Si click Droit
    if event.type == MOUSEBUTTONDOWN and event.button == 3:
         menuOuvert = True
         pos_menu_1_X = event.pos[0]
         pos_menu_1_Y = event.pos[1]

    #Si touche "Droite" ou "Gauche" utilisée
    if event.type == KEYUP:
        if event.key == K_a:
            print("Gauche")
            if choixMenu >0 :
                choixMenu= choixMenu-1
        if event.key == K_d:
            print("Droite")
            if choixMenu < nbMaxTourMenu :
                choixMenu= choixMenu+1
        if event.key == K_SPACE :
                print("Espace x: ",int(pos_menu_1_X/32), " y : ",int(pos_menu_1_Y/32))
                if collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]== 0:
                    print("On peu poser tourelle")
                    dessinTour = True
                    menuOuvert = False
                    collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]=1
                elif collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]== 1:
                    print("On NE peut PAS poser de tourelle !!!")
                    menuOuvert = False




# Initialisation des variables de la Carte
Map = [[0] * 28 for _ in range(61)]
Carte = [[0] * 32 for _ in range(25)]

x=0
# Mise en place de la carte avec les différentes tiles
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
def rot_center(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    rads = math.atan2(-dy,dx)
    rads %= 2*math.pi
    angle_d = math.degrees(rads)

    return angle_d


#Variable qui continue la boucle si = 1, stoppe si = 0

continuer = 1
pygame.display.flip()

inte= False


reste = 0
#Boucle infinie

while continuer:
    for i in range (0,32):
            for j in range (0,25):
                fenetre.blit(Carte[j][i], (i*LARGEUR_CASE,j*HAUTEUR_CASE))


    for i in range(len(tabTourelles)):
            fenetre.blit(tabTourelles[i],(tabTourelles_Pos_X[i],tabTourelles_Pos_Y[i]))

    

        
            
    for event in pygame.event.get():
        PoserTourelle(event)

        if event.type == QUIT:
            continuer = 0
            pygame.quit()


    


            
            #fenetre.blit(sbireHaut1,(33,0))
            #fenetre.blit(sbireBas1,(65,0))

    for i in range(len(tabTourelles)):
            if typeTourelle[i] == 1:
                tabTourelles[i] = tourelle_1
            elif typeTourelle[i] == 2:
                tabTourelles[i] = tourelle_2
            elif typeTourelle[i] == 3:
                tabTourelles[i] = tourelle_3

            tabTourelles[i].set_at((16, 36), (255,0,0,255))

            #angle = rot_center(event.pos[0],event.pos[1],(tabTourelles_Pos_X[i]),tabTourelles_Pos_Y[i])
            angle  = rot_center(sbiresManches[0].posX,sbiresManches[0].posY,(tabTourelles_Pos_X[i]),tabTourelles_Pos_Y[i])
            #rect = tourelle_1.get_rect(center=(16, 36))
            #rot_image = pygame.transform.rotate(tourelle_1, angle)
            #rot_rect = rot_image.get_rect(center=rect.center)
            #angle = math.atan2(event.pos[1] - tabTourelles_Pos_Y[i],event.pos[0] - tabTourelles_Pos_X[i] )* 57.296


            tabTourelles[i]= pygame.transform.rotate(tabTourelles[i],angle)
    temps = pygame.time.get_ticks()     #temps
    temps2 = temps - reste

    if (temps2 - vitesseSbires > 0):      # Chaque 500 ms le sbire se déplace

        reste += vitesseSbires
        temps2 = temps2 - reste
        for i in range(len(sbiresManches)):
            BougerSbire(sbiresManches[i])
    DessinerTourelles()
    DebutManche()


    for i in range(len(sbiresManches)):
        fenetre.blit(sbiresManches[i].img,(sbiresManches[i].posX+32,sbiresManches[i].posY))


    #Rafraichissement
    pygame.display.flip()

            
    continue #Je place continue ici pour pouvoir relancer la boucle infinie
                 #mais il est d'habitude remplacé par une suite d'instructions
