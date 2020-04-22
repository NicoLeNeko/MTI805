# From https://stackoverflow.com/a/55517239/7243716 or https://stackoverflow.com/questions/35176451/python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates#35178910
import numpy as np
import vg
import math

# From https://stackoverflow.com/a/17796482/7243716 or https://stackoverflow.com/questions/17796446/convert-a-list-to-a-string-and-back#17796482
from ast import literal_eval

# From https://stackoverflow.com/a/45028419/7243716 or https://stackoverflow.com/questions/45015268/how-do-i-pipe-output-of-one-python-script-to-another-python-script
import sys

import re


def main():
    # Nombre de cycle nécessaire pour envoyer un message (1 msg/4 cycles)
    PERIODICITY = 4
    cycles_without_sending = 0  # variable indiquant le cycle actuel

    # précompilation du regex, indication des motifs de mots à enlever
    regex = re.compile(r"prepro.*")
    last_angles = []
    while True:
        line = sys.stdin.readline()  # Lis ligne dans le pipelin stdin
        line = regex.sub("", line)  # enlève les motifs de mot prédeterminés de la string par substitution

        # si on a plus d'entrée
        if not line:
            break  # on sort de la boucle while (fin du programme)

        # si on a que des espaces blanc
        if line.isspace() or "[]" in line:
            continue  # on passe à la prochaine itération

        givenArray = literal_eval(line)[0]['coordinates']  # on extirpe seulement la liste les coordonnées de la string

        if len(givenArray) < 3:
            sys.stdout.write(repr(givenArray))
            sys.stdout.flush()
            continue

        # Extrait les coordonnées des 3 joints du bras gauche
        # a, b, c = np.array((givenArray[6],givenArray[8],givenArray[10]))

        # Extrait les coordonnées des 3 joints du bras droit
        a, b, c = np.array((givenArray[5], givenArray[7], givenArray[9]))

        # Vectors
        ab = b - a
        bc = c - b
        # Get angles on the 2D plane by projecting on it (z is the normal here)
        # TODO: Change when dealing with 3d later
        if np.any(ab!=0):
            angle1 = vg.signed_angle(ab, np.array((1, 0, 0)), vg.basis.neg_z)
        else:
            angle1= math.nan
        if np.any(bc!=0):
            angle2 = vg.signed_angle(bc, np.array((1, 0, 0)), vg.basis.neg_z)
        else:
            angle2 = math.nan

        # met a jour la liste de tous les angles calculés depuis la dernière période
        last_angles = update_liste_angles(last_angles, [angle1, angle2], PERIODICITY)
        # on incrémente le compteur de cycle sans message
        cycles_without_sending += 1
        # si le compteur de cycle correspond à n période
        if cycles_without_sending % PERIODICITY == 0:
            cycles_without_sending = 0  # on remet le compte à 0 pour ne pas dépasser la valeur max du type
            # calcule les angles avec la moyenne mobile
            angles_to_send = moyenne_mobile(last_angles)
            output_str = str(angles_to_send[0]) + " " + str(angles_to_send[1]) + "\n"

            # envoi l'information au prochain dans std out
            sys.stdout.write(output_str)
            sys.stdout.flush()  # force l'écriture en .vitant le buffering (pratique pour python2.7)


# Garde une liste a jour avec <les max_size> derniers elements
def update_liste_angles(liste_angles, new_elements, max_size):
    # on verifie si les angle ne sont pas nan
    for i, angle in enumerate(new_elements):
        # si l<angle est nan
        if math.isnan(angle):
            # si la liste n'est pas vide
            # print("angle ", i, "  was nan: ",angle)
            if len(liste_angles) > 1:
                # on prend sa derniere valeur connue
                new_elements[i] = liste_angles[-1][i]
            # sinon on met les valeurs a 0
            else:
                new_elements[i] = 0

    liste_angles.append(new_elements)
    while len(liste_angles) > max_size:
        liste_angles.pop(0)
    return liste_angles


def moyenne_mobile(list_angles):
    diviseur = len(list_angles)  # etabli le diviseur par le nombre de liste d'angles
    dim = len(list_angles[0])  # établi le nombre d'angles dans une liste d'angle
    final_angles = []  # tableau contenant les moyennes des angles

    # si on a qu'un seul angle
    if diviseur < 2:
        return list_angles

    # initialise la liste d'angles finaux à 0
    for i in range(dim):
        final_angles.append(0)

    # on calcule la moyenne de chaque angle
    for angles in list_angles:
        for i, angle in enumerate(angles):
            if angle != 0:
                final_angles[i] += angle / diviseur
            else:
                final_angles[i] += 0

    return final_angles


main()
