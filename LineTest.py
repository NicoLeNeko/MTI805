# Snake Tutorial Python

import math
import pygame

global PLAYWIDTH, ROWS, bras, snack, counterIter, INFOSPACE

PLAYWIDTH = 500  # taile en pixel de notre fenêtre carrée
INFOSPACE = 100  # taille de la baniere dinfo en pixel


class Arm(object):
    jointsPos = []
    longSeg1 = 200
    longSeg2 = 150

    def __init__(self):
        # self.longSeg1=200
        # self.longSeg2=150
        self.jointsPos.append([0, 0])
        self.jointsPos.append([self.longSeg1, 0])
        self.jointsPos.append([self.longSeg1, self.longSeg2])
        self.anglej1 = 0
        self.anglej2 = 0

    def move(self):
        # pour chaque évènnements
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
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

                if event.key == pygame.K_RIGHT:
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

                if event.key == pygame.K_UP:
                    if self.anglej2 == 359:
                        self.anglej2 = 0

                    else:
                        self.anglej2 += 1  # on bouge le joint 2

                if event.key == pygame.K_DOWN:
                    if self.anglej2 == 0:
                        self.anglej2 = 359
                    else:
                        self.anglej2 -= 1  # on bouge le joint 2

    def moveSegments(self):
        self.move()
        # bouge les segments selon les angles a jour
        angle1 = (self.anglej1 * 2 * math.pi) / 360
        angle2 = (self.anglej2 * 2 * math.pi) / 360
        self.jointsPos[1] = [self.longSeg1 * math.cos(angle1), self.longSeg1 * math.sin(angle1)]
        self.jointsPos[2] = [self.jointsPos[1][0] + self.longSeg2 * math.cos(angle2),
                             self.jointsPos[1][1] + self.longSeg2 * math.sin(angle2)]


def drawArm(jointPos, surface):
    center = [PLAYWIDTH / 2, PLAYWIDTH / 2 + INFOSPACE]
    xprec = 0
    yprec = 0
    # pour chaque joints
    for j in jointPos:

        if xprec != 0:
            xactu = j[0] + center[0]
            yactu = j[1] + center[1]
            pygame.draw.line(surface, (255, 255, 255), (xprec, yprec + INFOSPACE), (xactu, yactu + INFOSPACE),10)
            xprec = xactu
            yprec = yactu
        else:
            xprec = j[0] + center[0]
            yprec = j[1] + center[1]


# Fonction qui redessine tout ce qui se passe à l'écran (screen update)
def redrawWindow(surface):
    global ROWS, PLAYWIDTH, bras, snack
    surface.fill((0, 0, 0))  # on trace l'arrière plan
    drawArm(bras.jointsPos, surface)  # dessin bras
    showInfo(surface, bras)  # on affiche les infos comme le score et le nombre de pas
    pygame.display.update()  # on affiche tout (screen update)


def getInfo(infoBras):
    infos = [["angJoint1 : ", infoBras.anglej1], ["angJoint2 : ", infoBras.anglej2], ["Direction Y:", 2],
             ["position:", 2], ["# de pas:", 2], ["distance:", 2],
             ["Explored tiles:", 2], ["best direction", 2],
             ["left score:", 2], ["right score:", 2], ["up score:", 2]]
    return infos


def showInfo(surface, bras):
    global textSpots
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 128)
    numOfXSpots = 3
    numOfYSpots = 4
    infoToShow = getInfo(bras)

    # Création d'un tableau des positions pour le texte dans la banière
    if counterIter <= 1:
        spotX = 0
        spotY = 0
        spotHeight = INFOSPACE // numOfYSpots
        spotWidth = PLAYWIDTH // numOfXSpots
        textSpots = []
        for i in range(0, numOfXSpots):
            spotY = 0
            for j in range(0, numOfYSpots):
                textSpots.append((spotX, spotY))
                spotY += spotHeight
            spotX += spotWidth

    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    for ind, inf in enumerate(infoToShow):
        textSurfaceObj = fontObj.render(inf[0] + str(inf[1]), True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = textSpots[ind]
        surface.blit(textSurfaceObj, textRectObj)


def main():
    # permet d'utiliser ces variables en dehors du main()
    global PLAYWIDTH, ROWS, bras, counterIter, INFOSPACE

    PLAYWIDTH = 500  # taile en pixel de notre fenêtre carrée
    INFOSPACE = 100  # taille de la baniere dinfo en pixel

    pygame.init()
    pygame.key.set_repeat(10)
    win = pygame.display.set_mode((PLAYWIDTH, PLAYWIDTH + INFOSPACE))  # définition de la fenêtre
    bras = Arm()  # instanciation bras
    flag = True  # drapeau qui fait rouler le jeu

    clock = pygame.time.Clock()  # permet de gérer le temps des cycles
    counterIter = 0

    RUNNING, PAUSE = 0, 1
    state = RUNNING
    while flag:
        for event in pygame.event.get():
            # si on a appuyé sur la croix de la fenêtre
            if event.type == pygame.QUIT:
                pygame.quit()

            # ici on enregistre toutes les touches qui on été pressée pendant une itération du jeu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    state = PAUSE
                    printOnce = 1
                    pygame.key.set_repeat(0)
                elif event.key == pygame.K_p:
                    print("back in game")
                    state = RUNNING
                    pygame.key.set_repeat(10)
                elif event.key == pygame.K_q:
                    pygame.quit()

        if state == RUNNING:
            pygame.time.delay(20)  # on donne un délai de 50 ms entre chaque itération
            clock.tick(60)  # regule le fps max
            counterIter += 1
            bras.moveSegments()
            redrawWindow(win)

        elif state == PAUSE:
            if printOnce == 1:
                print("Game in pause")
                printOnce = 0


main()
