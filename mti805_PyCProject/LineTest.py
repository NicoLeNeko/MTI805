# Snake Tutorial Python

import sys
import math
import pygame

global PLAYWIDTH, ROWS, bras, INFOSPACE, firstTime

PLAYWIDTH = 500  # taile en pixel de notre fenêtre carrée
INFOSPACE = 100  # taille de la baniere dinfo en pixel
firstTime = True


class Arm(object):
    jointsPos = []  # liste des positions des joints du bras
    longSeg1 = 200  # longeur premier segment de bras
    longSeg2 = 150  # longeur 2e segment de bras (avant-bras)

    def __init__(self):
        self.jointsPos.append([0, 0])
        self.jointsPos.append([self.longSeg1, 0])
        self.jointsPos.append([self.longSeg1, self.longSeg2])
        self.anglej1 = 0
        self.anglej2 = 0

    # fonction pour bouger manuellement le bras
    def move_manu(self):
        # pour chaque évènnements
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:  # si on appuie sur une touche
                if event.key == pygame.K_LEFT:  # si on appuie sur fleche gauche
                    if self.anglej1 == 359:
                        self.anglej1 = 0
                        if self.anglej2 == 359:
                            self.anglej2 = 0
                        else:
                            self.anglej2 += 1  # on bouge le joint 2

                    else:
                        self.anglej1 += 1  # on bouge le joint 1
                        if self.anglej2 == 359:
                            self.anglej2 = 0
                        else:
                            self.anglej2 += 1  # on bouge le joint 2

                if event.key == pygame.K_RIGHT:  # si on appuie sur fleche droite
                    if self.anglej1 == 0:
                        self.anglej1 = 359
                        if self.anglej2 == 0:
                            self.anglej2 = 359
                        else:
                            self.anglej2 -= 1  # on bouge le joint 2
                    else:
                        self.anglej1 -= 1  # on bouge le joint 1
                        if self.anglej2 == 0:
                            self.anglej2 = 359
                        else:
                            self.anglej2 -= 1  # on bouge le joint 2

                if event.key == pygame.K_UP:  # si on appuie sur fleche en haut
                    if self.anglej2 == 359:
                        self.anglej2 = 0
                    else:
                        self.anglej2 += 1  # on bouge le joint 2

                if event.key == pygame.K_DOWN:  # si on appuie sur fleche gauche en bas
                    if self.anglej2 == 0:
                        self.anglej2 = 359
                    else:
                        self.anglej2 -= 1  # on bouge le joint 2

    # bouge les segments avec les touches du clavier
    def moveSegments(self):
        self.move_manu()  # appelle le mouvement par les touches de clavier, reçois des angles
        self.update_arm()  # bouge les segments du bras selon les angles a jour

    def update_arm(self):
        # calcul l'angle en Radian
        angle1 = (self.anglej1 * 2 * math.pi) / 360
        angle2 = (self.anglej2 * 2 * math.pi) / 360
        # Met à jour les positions selon les angles
        self.jointsPos[1] = [self.longSeg1 * math.cos(angle1), self.longSeg1 * math.sin(angle1)]
        self.jointsPos[2] = [self.jointsPos[1][0] + self.longSeg2 * math.cos(angle2),
                             self.jointsPos[1][1] + self.longSeg2 * math.sin(angle2)]

    # bouge le bras selon les angles reçus
    def doPose(self, angles):
        # S'assure que l'angle reçu n'est pas nul
        if not math.isnan(angles[0]):
            self.anglej1 = angles[0]
        if not math.isnan(angles[1]):
            self.anglej2 = angles[1]

        # bouge les segments du bras selon les angles a jour
        self.update_arm()


# Dessine le bras, l'épaule fixée à une position sur l'écran
def drawArm(jointPos, surface):
    xprec = 0  # coord x du joint précédent
    yprec = 0  # coord y du joint précédent
    decalage = [100, INFOSPACE + 100]  # décalage pour position de l'épaule
    colorSeg = [(255, 0, 0), (0, 255, 0)]  # couleur des segments
    # pour chaque joints
    for i, j in enumerate(jointPos):
        # si on n'est pas sur le premier joint (épaule)
        if xprec != 0:
            xactu = j[0] + decalage[0]  # on ajuste la coordonnée pour la position d'affichage
            yactu = j[1] + decalage[1]
            # on dessine le segment avec sa couleur désignée
            pygame.draw.line(surface, colorSeg[i - 1], (xprec, yprec + INFOSPACE), (xactu, yactu + INFOSPACE), 10)
            xprec = xactu  # les coordonnées actuelle deviennent les précédentes pour le prochain joint
            yprec = yactu

        # Sinon on fixe l'épaule à son point d'ancrage
        else:
            xprec = j[0] + decalage[0]
            yprec = j[1] + decalage[1]


# Fonction qui redessine tout ce qui se passe à l'écran (screen update)
def redrawWindow(surface, textSpot):
    global ROWS, PLAYWIDTH, bras
    surface.fill((0, 0, 0))  # on trace l'arrière plan
    drawArm(bras.jointsPos, surface)  # dessin bras
    showInfo(surface, bras, textSpot)  # on affiche les infos comme les angles du bras
    pygame.display.update()  # on affiche tout (screen update)


# Regroupe les informations qui seront affichées
def getInfo(infoBras):
    infos = [["angJoint1 : ", infoBras.anglej1], ["angJoint2 : ", infoBras.anglej2], ["Direction Y:", 2],
             ["position:", 2], ["X joint1 : ", bras.jointsPos[1][0]], ["Y joint1 : ", bras.jointsPos[1][1]],
             ["X joint2 : ", bras.jointsPos[2][0]], ["Y joint2 : ", bras.jointsPos[2][1]]]
    return infos


# Crée la bannière de la fenêtre et écrit les informations dans celle-ci
def showInfo(surface, obj_bras, textSpot):
    GREEN = (0, 255, 0)
    infoToShow = getInfo(obj_bras)  # va chercher la liste de texte à afficher

    fontObj = pygame.font.Font('freesansbold.ttf', 20)  # définition de la police
    # pour chaque information dans la liste d'informations
    for ind, inf in enumerate(infoToShow):
        # on crée un objet de surface pour afficher le texte
        textSurfaceObj = fontObj.render('{0}{1:0.1f}'.format(inf[0], inf[1]), True, GREEN)
        textRectObj = textSurfaceObj.get_rect()  # on extrait l'aire requise (rectangle)
        textRectObj.topleft = textSpot[ind]  # on extrait la position du coin haut gauche du rectangle
        surface.blit(textSurfaceObj, textRectObj)  # affiche le rectangle contenant l'information


# Création d'un tableau des positions pour le texte dans la banière
def init_textSpot():
    numOfXSpots = 2  # quantités de colonnes
    numOfYSpots = 4  # qte de lignes
    spotX = 0  # coordonnée X du point d'ancrage
    spotHeight = INFOSPACE // numOfYSpots  # incrément de hauteur d'une ligne
    spotWidth = PLAYWIDTH // numOfXSpots  # incrément de largeur d'une ligne
    textSpots = []  # liste des points d'ancrages

    # Génération des points d'ancrages
    for i in range(0, numOfXSpots):
        spotY = 0
        for j in range(0, numOfYSpots):
            textSpots.append((spotX, spotY))
            spotY += spotHeight
        spotX += spotWidth
    return textSpots


def main():
    # permet d'utiliser ces variables en dehors du main()
    global PLAYWIDTH, ROWS, bras, INFOSPACE

    PLAYWIDTH = 500  # taile en pixel de notre fenêtre carrée
    INFOSPACE = 100  # taille de la baniere dinfo en pixel

    pygame.init()  # démmare pygame
    pygame.key.set_repeat(10)  # permet de garder un touche enfoncé, avec 10 ms entre chaque entrée
    win = pygame.display.set_mode((PLAYWIDTH, PLAYWIDTH + INFOSPACE))  # définition de la fenêtre
    bras = Arm()  # instanciation bras
    flag = True  # drapeau qui fait rouler le jeu

    piped_mode = True  #bool pour utilisation du pipeline
    clock = pygame.time.Clock()  # permet de gérer le temps des cycles

    textSpot = init_textSpot()   #initialise les positions d'ancrages pour la baniere d<info

    RUNNING, PAUSE = 0, 1   #definition des etats
    state = RUNNING #on commence avec le jeu actif
    while flag:
        #Pour chaque événement pygame (clic, clavier,boutons)
        for event in pygame.event.get():
            # si on a appuyé sur la croix de la fenêtre
            if event.type == pygame.QUIT:
                pygame.quit()   #on quitte (met fin au programme)

            # ici on enregistre toutes les touches qui on été pressée pendant une itération du jeu
            if event.type == pygame.KEYDOWN:
                #si on appuie sur sur s on stop le jeu (pause)
                if event.key == pygame.K_s:
                    state = PAUSE
                    printOnce = 1
                    pygame.key.set_repeat(0)
                #si on appuie sur p on play le jeu (running)
                elif event.key == pygame.K_p:
                    print("back in game")
                    state = RUNNING
                    pygame.key.set_repeat(10)
                #si on appuie sur q on quitte le jeu (+ efficace que bouton)
                elif event.key == pygame.K_q:
                    pygame.quit()

        #Si le jeu roule
        if state == RUNNING:
            pygame.time.delay(50)  # on donne un délai de 20 ms entre chaque itération
            clock.tick(60)  # regule le fps max
            #si on utilise le pipeline pour les commandes
            if piped_mode:
                line = sys.stdin.readline()  #on lis une ligne du pipeline (libère la ligne du pipe)
                #Si la ligne ne contient rien on passe à la prochaine itération
                if not line:
                    continue
                #sinon on sépare les segments de la ligne
                line_split = line.split()
                angles=list(map(float, line_split))  # extrait les angles de la ligne

                print("angles", angles)
                bras.doPose(angles) #on commande le bras avec les angles

            #Sinon on est en mode manuel avec le clavier
            else:
                bras.moveSegments()

            #on met l'interface graphique à jour
            redrawWindow(win, textSpot)

        elif state == PAUSE:
            if printOnce == 1:
                print("Game in pause")
                printOnce = 0


main()
