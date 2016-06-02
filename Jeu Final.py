#Importation des bibliothèques nécessaires

import pygame
import math
from pygame.locals import *
from math import sqrt
#On ouvre le fichier "first" afin de voir si c'est la première fois que le programme est executé
first  = open("Ressources/first.txt",'r')
cont_first = first.read()
first.close()
print(cont_first)
if cont_first == "oui" :
    import menu

# Importation des bibliothèques pour redémarrer le programme
import sys
import os


# ajouter vie nexus
# mahammt finir
# Metre 30 sec debut ensuite 5 sec


#On ouvre le fichier pour avoir les valeurs des variables
#à utiliser selon la manche dans laquelle on est
txt = open("Ressources/variables.txt",'r')
cont_text = txt.read()
txt_split = cont_text.split()
txt.close()



pygame.init()

#On Ouvre l'ensemble des sbires en une image que l'on va découper
# sbireDroite1 quand le sbire met le pied droit en avant
# sbireDroite2 uand le sbire met le pied gauche ne avant par exemple
sbireEntier = pygame.image.load("Ressources/sbire_1.png")
Bar= pygame.image.load("Ressources/Barre.png")
sbireDroite1 =sbireEntier.subsurface(0 *32,2*32,32,32)
sbireHaut1 =sbireEntier.subsurface(0 *32,3*32,32,32)
sbireBas1 =sbireEntier.subsurface(0 *32,0*32,32,32)

sbireDroite2 =sbireEntier.subsurface(2 *32,2*32,32,32)
sbireHaut2 =sbireEntier.subsurface(2 *32,3*32,32,32)
sbireBas2 = sbireEntier.subsurface(2 *32,0*32,32,32)

#Variables de la fenetre + création
LARGEUR_CASE =32
HAUTEUR_CASE= 32
LARGEUR_FENETRE = 32* 32
HAUTEUR_FENETRE = 25 * 32
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))#,FULLSCREEN)
pygame.display.set_caption('Tower Defense ')

# On ouvre le son des tourelles et on baisse leur volume
son=pygame.mixer.Sound("Ressources/son_tire.ogg")
son.set_volume(0.05)


class Game :
    """ Classe Game qui va contenir les variables générales du jeu
        afin de les utiliser ultérieurement
    """
    global fenetre
    global txt_split
    def __init__(self):
        self.vie = 100
        # Les 4 prochaines variables dépendent de la manche actuelle
        self.manche = int(txt_split[2])
        self.argent = int(txt_split[1])
        self.vitesseSbires = int(txt_split[3]) #150
        self.nbSbireManche = int(txt_split[0])
        self.barreDeVie = pygame.draw.rect(fenetre,(0,255,0),(400,2,int(self.vie*1.5),15))
        self.mancheCommencee = False

class Sbire:
    """ Classe sbire qui permet la création de ces derniers
    avec différentes variables
    """
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
        self.couleurVie= (0,255,0)
        self.img = sbireDroite1
        self.spawn = False
        self.vie = 100
        self.enVie = True
        self.barreDeVie = pygame.draw.rect(fenetre,self.couleurVie,(self.posX+32,self.posY,int(self.vie*32/100),2))
    # Fonction qui dessine la barre de vie et change sa
    # couleur en fonction des pv
    def DessinerVie(self):
                if self.vie <33 :
                    self.couleurVie = (255,0,0)
                if self.vie <= 66 and self.vie >=33 :
                    self.couleurVie = (255,125,0)
                if self.vie >66 :
                    self.couleurVie = (0,255,0)

                self.barreDeVie =  pygame.draw.rect(fenetre,self.couleurVie,(self.posX+32,self.posY,int(self.vie*32/100),2))
# Création de la variable Jeu
Jeu = Game()




#On ouvre le ficher contenant les informations sur les collisions
collisions_fichier = open("Ressources/collisions.lvl", "r")
collisions_text = collisions_fichier.read()
collisions_fichier.close()
collisions = collisions_text.split()
collisions_liste=[[0] * 32 for _ in range(25)]

# On ouvre le fichier contenant les informations sur le cemin des sbires
chemin_fichier = open("Ressources/chemin.lvl", "r")
chemin_text = chemin_fichier.read()
chemin_fichier.close()
chemin = chemin_text.split()
chemin_liste=[[0] * 32 for _ in range(25)]



# Direction du sbire :
# Droite : 6
# Gauche : 4
# Bas : 5
# Haut : 8
directionSbire = 6


#On navigue dans la liste contenant les valeurs "0000" ou "0001" puis on crée un nouveau
# tableau 2D d'entiers avec '0' ou '1'
# 0 : On peut poser une tourelle
# 1 : On ne peut pas poser de tourelle
# Ces 3 variables permettent de naviguer facilement dans le tableau
y_col=0
x_col=0
inc=0
for i in range (0,25):
    for j in range (0,32):
        if collisions[inc] == "0000":
            collisions_liste[i][j]= 0
        elif collisions[inc] == "0001":
            collisions_liste[i][j]= 1
        inc=inc+1
# Idem, on navigue dans le contenu du fichier
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





#On ouvre le niveau.lvl et on lit ce qui y est écrit
monLvl = open("Ressources/monNiv.lvl", "r")
contenu = monLvl.read()
monLvl.close()
lvl = contenu.split()

# Numéro de la tourelle séléctionée ( dans le menu )
choixMenu = 0
menuOuvert = False

#On charge des images
grdeMap = pygame.image.load("Ressources/Sprites_Env.png")
menu_1 = pygame.image.load("Ressources/Menu_1.png")
tourelles_E =  pygame.image.load("Ressources/tourelles.png")
tourelles_Feu_E = pygame.image.load("Ressources/tourelles_feu.png")

# On charge l'image des sbores



# On découpe l'image pour avoir les différentes tourelles
tourelle_1 = tourelles_E.subsurface(42,0,53,31)
tourelle_2 = tourelles_E.subsurface(258,0,32,30)
tourelle_3 = tourelles_E.subsurface(0,0,41,31)

# On crée les images des tourelles qui tirent :
tourelle_feu_1 = tourelles_Feu_E.subsurface(42,0,53,31)
tourelle_feu_2 = tourelles_Feu_E.subsurface(258,0,32,30)
tourelle_feu_3 = tourelles_Feu_E.subsurface(0,0,41,31)

# Création des tourelles du menu ( afin de pouvoir utiliser la transparence)
tourelle_1m = tourelle_1.convert()
tourelle_2m = tourelle_2.convert()
tourelle_3m = tourelle_3.convert()

#Tableau de tourelles et de leurs attributs :
tabTourelles = []
tabTourelles_Pos_X = []
tabTourelles_Pos_Y = []
typeTourelle = []
focusTourelle=[]
activeTourelle=[]
#Position du menu
pos_menu_1_X = -1
pos_menu_1_Y = -1


nbMaxTourMenu = 3-1
dessinTour = False

# Intervalle de temps entre 2 apparitions
# On  1000 (ms) =  1 seconde avec le module temps
deltaTSpawn = 0 # Intervalle entre 2 apparition de sbires
numManche = 1
nbSbiresMax = int(txt_split[0])
nbSbireAct=0
vitesseSbires = 150
tps_feu = []
tps_feu2 = []
reste_feu = []
intervalle= []
# Création de la liste des sbires :
sbiresManches = []
# Liste des sbires vivants
sbireVivants = []

# Est-ce qu'on dessine le bout rouge des tourelle ?
dessinerRouge = False

premiereFois = [] # Ce tableau permet d'aviter les décalages de temps lors de la création d'une tourelle
inter = 0
interv=0
uneFois= False
interDeb = pygame.time.get_ticks()
vieAEnlever = 0
vitesseTire = 0
def Rotation_Tourelles(posX1,posY1,posX2,posY2):
    """
    Retourne l'angle entre 2 points que l'on convertie
    en degrés
    """
    distanceX = posX2 - posX1
    distanceY = posY2 - posY1
    radian = math.atan2(-distanceY,distanceX)
    radian %= 2*math.pi
    angle = math.degrees(radian)

    return angle
def restart_program():
    """Fonction qui permet de redémarrer le programme à chaque fois qu'une manche est terminée."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
def DebutManche():
    global interDeb
    global deltaTSpawn
    global sbiresManches
    global nbSbiresMax
    global nbSbireAct
    global Jeu
    global inter
    global finManche
    if TempsRestant() <= 0 : # Si on a attendu le temps d'intervalle entre 2 manches


        if Jeu.mancheCommencee == True :
            tps = pygame.time.get_ticks()-inter +1500-interDeb  #On enlève le décalage due à l'intervalle entre 2 manches
        if Jeu.mancheCommencee == False :
            inter = pygame.time.get_ticks()-interDeb
            tps = pygame.time.get_ticks()





        tps2 = tps - deltaTSpawn

        if (tps2 - 1500 > 0) and nbSbireAct < nbSbiresMax:
            if finManche == False :
                # Si la manche n'est pas terminée et que l'on a pas dépassé
                # le nombre de sbires à créer, on continue
                deltaTSpawn += 1500
                tps2 = tps2 - deltaTSpawn
                # A chaque fois on crée un nouveau sbire et on ajoute une case
                # dans sbireVivant liée au sbire précedemment créé
                sbireTemp = Sbire()
                sbiresManches.append(sbireTemp)
                sbireVivants.append(True)
                nbSbireAct +=1
                Jeu.mancheCommencee  = True
def TempsRestant():
        """
        Fonction qui permet de voir le temps qui sécoule afin de voir
        si l'on peut commencer la manche ou non
        """
        global interv
        global finManche
        global uneFois

        if finManche == True and uneFois == False:
            interv +=  int(pygame.time.get_ticks()/1000)
            uneFois = True


        temps = 10-int(pygame.time.get_ticks()/1000)+ interv
        if temps <= 0:
            temps =0

        return temps
def Ecrire(texte):
    font = pygame.font.SysFont("Arial",50)
    texteAffiche = font.render(texte,True,(0,0,0))
    return texteAffiche
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
            focusTourelle.append(0)
            activeTourelle.append(False)
            premiereFois.append(True)
            tps_feu.append(0)
            tps_feu2.append(0)
            reste_feu.append(0)
            intervalle.append(0)
        elif choixMenu == 1:
            tabTourelles.append(tourelle_2)
            typeTourelle.append(2)
            focusTourelle.append(0)
            activeTourelle.append(False)
            premiereFois.append(True)
            tps_feu.append(0)
            tps_feu2.append(0)
            reste_feu.append(0)
            intervalle.append(0)
        elif choixMenu == 2:
            tabTourelles.append(tourelle_3)
            typeTourelle.append(3)
            focusTourelle.append(0)
            activeTourelle.append(False)
            premiereFois.append(True)
            tps_feu.append(0)
            tps_feu2.append(0)
            reste_feu.append(0)
            intervalle.append(0)

       # tabTourelles.append(tourelle_1)
        tabTourelles_Pos_X.append(int(pos_menu_1_X/32)*32-15+16)
        tabTourelles_Pos_Y.append(int(pos_menu_1_Y/32)*32-37+16)
        dessinTour=False
    for i in range(len(tabTourelles)):
            fenetre.blit(tabTourelles[i],(tabTourelles_Pos_X[i],tabTourelles_Pos_Y[i]))
def BougerSbire( sbire):
    global direction
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

    #print("direction : ",sbire.direction)
    #print( " X : ",int(sbire.posX/32)," Y : ",int(sbire.posY/32))
    #print(" chemin : ",chemin_liste[int((sbire.posY/32))][int((sbire.posX+32)/32)+1])

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
    global Jeu
    # Si click Droit
    if event.type == MOUSEBUTTONDOWN and event.button == 3:
         menuOuvert = True
         pos_menu_1_X = event.pos[0]
         pos_menu_1_Y = event.pos[1]

    #Si touche "Droite" ou "Gauche" utilisée
    if event.type == KEYUP:
        if event.key == K_a:
            #print("Gauche")
            if choixMenu >0 :
                choixMenu= choixMenu-1
        if event.key == K_d:
            #print("Droite")
            if choixMenu < nbMaxTourMenu :
                choixMenu= choixMenu+1
        if event.key == K_SPACE :
            #print("dedans")
            #print("Espace x: ",int(pos_menu_1_X/32), " y : ",int(pos_menu_1_Y/32))
            if collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]== 0:
                if choixMenu ==0 and Jeu.argent >= 25:
                    dessinTour = True
                    menuOuvert = False
                    collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]=1
                    Jeu.argent -= 25
                if choixMenu ==1 and Jeu.argent >= 50:
                    dessinTour = True
                    menuOuvert = False
                    collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]=1
                    Jeu.argent -= 50
                if choixMenu ==2 and Jeu.argent >= 75:
                    dessinTour = True
                    menuOuvert = False
                    collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]=1
                    Jeu.argent -= 75
                    #print("On peu poser tourelle")

                if choixMenu ==0 and Jeu.argent < 25:
                    menuOuvert = False
                if choixMenu ==1 and Jeu.argent < 50:
                    menuOuvert = False
                if choixMenu ==2 and Jeu.argent < 75:
                    menuOuvert = False

            elif collisions_liste[int(pos_menu_1_Y/32)][int(pos_menu_1_X/32)]== 1:
                #print("On NE peut PAS poser de tourelle !!!")
                menuOuvert = False
def ViserSbire(tourellePosX,tourellePosY,nb):
    global focusTourelle
    global sbiresManches


    for i in range(len(sbiresManches)):
        if focusTourelle[nb] <= (len(sbiresManches)-1):

            distance = sqrt(pow((tourellePosX-sbiresManches[focusTourelle[nb]].posX),2)+pow((tourellePosY-sbiresManches[focusTourelle[nb]].posY),2))
            if distance <=250:
                #print("en vie le : ",focusTourelle[nb]," : ",sbiresManches[focusTourelle[nb]].enVie)
                if sbiresManches[focusTourelle[nb]].enVie== False:
                    #print("euuuuuh ???")
                    focusTourelle[nb]+=1
                elif sbiresManches[focusTourelle[nb]].enVie== True:

                    angle2  = Rotation_Tourelles(sbiresManches[focusTourelle[nb]].posX,sbiresManches[focusTourelle[nb]].posY,tourellePosX,tourellePosY)
                    activeTourelle[nb] = True
                    return angle2
            elif distance > 250:
                #print("on ne vise personne !")
                focusTourelle[nb] +=1
                if focusTourelle[nb] > (len(sbiresManches)-1):
                    focusTourelle[nb] =0
                activeTourelle[nb] = False

                return 0
def Tirer(nb):
    global activeTourelle

    return activeTourelle[nb]
def Feu(nb):
    global reste_feu
    global dessinerRouge
    global intervalle
    global premiereFois
    global tps_feu
    global tps_feu2
    global reste_feu
    global intervalle
    global son
    global vieAEnlever
    global vitesseTire
    #print(" La tourelle numéro : ",nb," attaque !")
    if premiereFois[nb] == True:
        intervalle[nb] = pygame.time.get_ticks()
        premiereFois[nb] = False

    tps_feu[nb] = pygame.time.get_ticks()- intervalle[nb]     #temps
    tps_feu2[nb] = tps_feu[nb] - reste_feu[nb]
    if typeTourelle[nb] == 1 :
        vitesseTire = 500
    if typeTourelle[nb] == 2 :
        vitesseTire = 450
    if typeTourelle[nb] == 3 :
        vitesseTire = 400
    if tps_feu2[nb] - vitesseTire > 0:      # Chaque 500 ms le sbire se déplace
        #print("Attaque ! : ",nb)
        #print(" reste : ", reste_feu)
        reste_feu[nb] += vitesseTire
        tps_feu2[nb] = tps_feu2[nb] - reste_feu[nb]
        dessinerRouge = True

        if activeTourelle[nb] == True :
            if typeTourelle[nb] == 1 :
                vieAEnlever = 10
            if typeTourelle[nb] == 2 :
                vieAEnlever = 15
            if typeTourelle[nb] == 3 :
                vieAEnlever = 20
            #print("on enleve des pv")
            son.play()
            print("vie A enlever : ",vieAEnlever)
            sbiresManches[focusTourelle[nb]].vie -= vieAEnlever
            if sbiresManches[focusTourelle[nb]].vie <= 0:
                sbiresManches[focusTourelle[nb]].vie =0

    return  dessinerRouge



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
        x += 1

#Rotation de la fenêtre



#Variable qui continue la boucle si = 1, stoppe si = 0

continuer = 1
pygame.display.flip()

inte= False

finManche = False
reste = 0
#Boucle infinie

while continuer:
    for i in range (0,32):
            for j in range (0,25):
                fenetre.blit(Carte[j][i], (i*LARGEUR_CASE,j*HAUTEUR_CASE))


    for i in range(len(tabTourelles)):
            fenetre.blit(tabTourelles[i],(tabTourelles_Pos_X[i],tabTourelles_Pos_Y[i]))
    fenetre.blit(Bar, (0,0))
    fenetre.blit(Ecrire(str(Jeu.manche)),(920,0-2))
    fenetre.blit(Ecrire(str(TempsRestant())),(720,0-2))
    fenetre.blit(Ecrire(str(Jeu.argent)),(300,0-2))
    fenetre.blit(Ecrire(str(Jeu.nbSbireManche)),(100,0-2))
    Jeu.barreDeVie = pygame.draw.rect(fenetre,(0,255,0),(420,15,int(Jeu.vie*1.5),15))



    for event in pygame.event.get():
        PoserTourelle(event)

        if event.type == QUIT:
            first2 = open("Ressources/first.txt",'w')
            first2.write("oui")
            first2.close()
            continuer = 0
            pygame.quit()






            #fenetre.blit(sbireHaut1,(33,0))
            #fenetre.blit(sbireBas1,(65,0))

    for i in range(len(tabTourelles)):
        #print("FinManche : ",finManche)
        if finManche == False :
            if Tirer(i) == False :
                if typeTourelle[i] == 1:
                    tabTourelles[i] = tourelle_1
                elif typeTourelle[i] == 2:
                    tabTourelles[i] = tourelle_2
                elif typeTourelle[i] == 3:
                    tabTourelles[i] = tourelle_3
            elif Tirer(i) == True:
                if typeTourelle[i] == 1:
                    tabTourelles[i] = tourelle_feu_1
                elif typeTourelle[i] == 2:
                    tabTourelles[i] = tourelle_feu_2
                elif typeTourelle[i] == 3:
                    tabTourelles[i] = tourelle_feu_3
            #print("au bah didier ?")
            Feu(i)

            Tirer(i)
        if finManche == True :
            if typeTourelle[i] == 1:
                tabTourelles[i] = tourelle_1
            elif typeTourelle[i] == 2:
                tabTourelles[i] = tourelle_2
            elif typeTourelle[i] == 3:
                tabTourelles[i] = tourelle_3



        if len(sbiresManches) >0:
            if sbireVivants.count(False) == len(sbireVivants):
                #print(" ils dsont tous mort !")
                finManche = True

                txt = open("Ressources/variables.txt",'w')
                txt.write(str(nbSbiresMax+2))
                txt.write(" "+str(Jeu.argent))
                txt.write(" "+str(Jeu.manche+1))
                if Jeu.vitesseSbires-5 <= 15 :
                    txt.write(" "+"15")
                elif Jeu.vitesseSbires-5 > 15 :
                    txt.write(" "+str(Jeu.vitesseSbires-5))
                txt.close()
                restart_program()

                print("leleleleoeledleflefleflelfelfledledledlledell")
                #import Test1.py
            elif sbireVivants.count(False) != len(sbireVivants):

                finManche = False


            #print("Est -ce que les sbires son vivantts ? : ",finManche)
            if finManche == False and sbireVivants.count(False) != len(sbireVivants) :
                tabTourelles[i]= pygame.transform.rotate(tabTourelles[i],ViserSbire(tabTourelles_Pos_X[i],tabTourelles_Pos_Y[i],i))





    temps = pygame.time.get_ticks()     #temps
    temps2 = temps - reste

    if temps2 - Jeu.vitesseSbires > 0:      # Chaque 500 ms le sbire se déplace

        reste += Jeu.vitesseSbires
        temps2 = temps2 - reste
        for i in range(0,len(sbiresManches)):
            if sbireVivants[i] == True :
                BougerSbire(sbiresManches[i])
    DessinerTourelles()
    DebutManche()

    #print("taille sbiresmanche : ",len(sbiresManches))
    for i in range(0,len(sbiresManches)):
        if sbiresManches[i].vie != 0 :
            fenetre.blit(sbiresManches[i].img,(sbiresManches[i].posX+32,sbiresManches[i].posY))
            sbiresManches[i].DessinerVie()
        elif sbiresManches[i].vie == 0 :
            if sbireVivants[i] == True:
                Jeu.nbSbireManche -=1
                Jeu.argent +=25
            sbireVivants[i] = False
            sbiresManches[i].enVie = False
        #print("Vie : ",sbiresManches[0].vie)



    #Rafraichissement
    pygame.display.flip()


    continue #Je place continue ici pour pouvoir relancer la boucle infinie
                 #mais il est d'habitude remplacé par une suite d'instructions
print(" FINIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")