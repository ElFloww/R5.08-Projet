import matplotlib.pyplot as plt
import cv2
import random
import keyboard
import simpleaudio as sa
import numpy as np
import math
import time


def CalculDistance(x1, y1, x2, y2):
    """
    Cette fonction permets de calculer la distance entre deux points
    :param x1: Propriété x du point 1
    :param y1: Propriété y du point 1
    :param x2: Propriété x du point 2
    :param y2: Propriété y du point 2
    :return: la distance entre les deux points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def PlayAudio(distance, TailleMaxImage):
    """
    Cette fonction permets de jouer un son en fonction de la distance
    :param distance: la distance qui va permettre de calculer la fréquence
    """

    # Définition des valeurs
    A = 1
    frequence = TailleMaxImage - distance + 1
    duree = 0.5
    taux_echantillonnage = 44100

    # Création du tableau pour faire evoluer notre sinosoidale en fonction du temps
    temps = np.linspace(0, duree, int(taux_echantillonnage * duree), endpoint=False)
    # Calcul de notre son
    sinusoidale = A * np.sin(2 * np.pi * frequence * temps)

    # Sérialisation
    audio = np.hstack(sinusoidale)
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)

    # On joue le son
    play_obj = sa.play_buffer(audio, 1, 2, taux_echantillonnage)

    # On attend que le son soit fini
    play_obj.wait_done()


def UpdateGame(xPosition, yPosition, hauteur, largeur, xHistoriquePosition, yHistoriquePosition, Distance, ):
    # On ajoute les coordonnées du nouveau point
    xHistoriquePosition.append(xPosition)
    yHistoriquePosition.append(yPosition)

    #On recherche le plus long entre la longueur et la largeur
    TailleMaxImage = hauteur
    if TailleMaxImage < largeur:
        TailleMaxImage = largeur

    #Si on est proche du bord
    if xPosition <= 100 or xPosition > largeur - 100 or yPosition <= 100 or yPosition > hauteur - 100:
        #On joue deux sons moyen
        PlayAudio(TailleMaxImage/2, TailleMaxImage)
        PlayAudio(TailleMaxImage/2, TailleMaxImage)

    # On joue le son associé
    PlayAudio(Distance, TailleMaxImage)


if __name__ == '__main__':
    # Définitions des variables importantes
    TempsJeu = 60

    Vitesse = 25
    # Lecture de l'image
    Image = cv2.imread("images/Plan_Amiens.JPG")
    # Récupération de la hauteur et de la largeur de l'image
    hauteur, largeur = Image.shape[:2]

    # Création du point caché via des valeurs aléatoire
    xPointCache = random.randint(0, largeur - 50)
    yPointCache = random.randint(0, hauteur - 50)

    # Définition du point de départ au milieu de l'image
    xPosition = largeur // 2
    yPosition = hauteur // 2

    # Création de l'historique des points
    xHistoriquePosition = []
    yHistoriquePosition = []

    # On ajoute le point de départ
    xHistoriquePosition.append(xPosition)
    yHistoriquePosition.append(yPosition)

    Distance = float('inf')

    # On définit notre temps avant le lancement du jeu
    TempsDebut = time.time()

    Termine = False
    while not Termine:
        if keyboard.is_pressed('up'):
            # On diminie notre ordonnée
            if yPosition - Vitesse > 0:
                yPosition -= Vitesse
                Distance = CalculDistance(xPosition, yPosition, xPointCache, yPointCache)
                UpdateGame(xPosition, yPosition, hauteur, largeur, xHistoriquePosition, yHistoriquePosition, Distance)

        if keyboard.is_pressed('down'):
            # On augmente notre ordonnée
            if yPosition + Vitesse < hauteur:
                yPosition += Vitesse
                Distance = CalculDistance(xPosition, yPosition, xPointCache, yPointCache)
                UpdateGame(xPosition, yPosition, hauteur, largeur, xHistoriquePosition, yHistoriquePosition, Distance)

        if keyboard.is_pressed('left'):
            # On diminue notre abscisse
            if xPosition - Vitesse > 0:
                xPosition -= Vitesse
                Distance = CalculDistance(xPosition, yPosition, xPointCache, yPointCache)
                UpdateGame(xPosition, yPosition, hauteur, largeur, xHistoriquePosition, yHistoriquePosition, Distance)
        if keyboard.is_pressed('right'):
            if xPosition + Vitesse < largeur:
                xPosition += Vitesse
                Distance = CalculDistance(xPosition, yPosition, xPointCache, yPointCache)
                UpdateGame(xPosition, yPosition, hauteur, largeur, xHistoriquePosition, yHistoriquePosition, Distance)

        if (time.time() - TempsDebut) > TempsJeu:
            print("Le temps est écoulé")
            Termine = True

        if Distance < 25:
            print("Vous avez trouvé l'objet")
            Termine = True

        if keyboard.is_pressed('q'):
            print('Vous avez abandonné')
            Termine = True
    plt.imshow(Image)
    plt.plot(xHistoriquePosition, yHistoriquePosition, "r-")
    plt.plot(xPosition, yPosition, "ro")
    plt.plot(xPointCache, yPointCache, "bo")
    plt.show()