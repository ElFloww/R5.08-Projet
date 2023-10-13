import matplotlib.pyplot as plt
import cv2
import random
import keyboard
import simpleaudio as sa
import numpy as np
import math


def CalculDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def PlayAudio(distance):
    A = 1
    frequence = 1500 - distance
    duree = 1
    taux_echantillonnage = 44100

    temps = np.linspace(0, duree, int(taux_echantillonnage * duree), endpoint=False)
    sinusoidale = A * np.sin(2 * np.pi * frequence * temps)

    audio = np.hstack(sinusoidale)
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)

    play_obj = sa.play_buffer(audio, 1, 2, taux_echantillonnage)
    play_obj.wait_done()


if __name__ == '__main__':
    image = cv2.imread("images/Plan_Amiens.JPG")
    hauteur, largeur = image.shape[:2]


    xPointCache = random.randint(0, largeur)
    yPointCache = random.randint(0, hauteur)
    xDepart = largeur // 2
    yDepart = hauteur // 2

    xHistoriquePosition = []
    yHistoriquePosition = []
    xHistoriquePosition.append(xDepart)
    yHistoriquePosition.append(yDepart)

    plt.imshow(image)
    plt.plot(xDepart, yDepart, "ro")
    plt.plot(xPointCache, yPointCache, "bo")
    plt.show()

    vitesse = 25

    distance = float('inf')

    termine = False
    while not termine:
        if keyboard.is_pressed('up'):
            yDepart -= vitesse
            distance = CalculDistance(xDepart, yDepart, xPointCache, yPointCache)
            xHistoriquePosition.append(xDepart)
            yHistoriquePosition.append(yDepart)
            PlayAudio(distance)

        if keyboard.is_pressed('down'):
            yDepart += vitesse
            distance = CalculDistance(xDepart, yDepart, xPointCache, yPointCache)
            xHistoriquePosition.append(xDepart)
            yHistoriquePosition.append(yDepart)
            PlayAudio(distance)

        if keyboard.is_pressed('left'):
            xDepart -= vitesse
            distance = CalculDistance(xDepart, yDepart, xPointCache, yPointCache)
            xHistoriquePosition.append(xDepart)
            yHistoriquePosition.append(yDepart)
            PlayAudio(distance)

        if keyboard.is_pressed('right'):
            xDepart += vitesse
            distance = CalculDistance(xDepart, yDepart, xPointCache, yPointCache)
            xHistoriquePosition.append(xDepart)
            yHistoriquePosition.append(yDepart)
            PlayAudio(distance)

        if distance < 25:
            print("Vous avez trouvé l'objet")
            plt.imshow(image)
            plt.plot(xHistoriquePosition, yHistoriquePosition, "r-")
            plt.plot(xDepart, yDepart, "ro")
            plt.plot(xPointCache, yPointCache, "bo")
            plt.show()
            termine = True

        if keyboard.is_pressed('q'):
            print('Fin du programme')
            termine = True
