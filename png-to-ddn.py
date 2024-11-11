import os
import imageio
import easygui
import tkinter as tk
from tkinter import colorchooser
import numpy as np
import subprocess

# Fonction pour ouvrir le sélecteur de couleur
def select_color():
    # Ouvre une fenêtre pour sélectionner une couleur
    color_code = colorchooser.askcolor(title="Choisir la couleur à supprimer")[0]
    if color_code:
        return tuple(map(int, color_code))  # Retourne la couleur sous forme de tuple (R, G, B)
    else:
        return None

# Ouvrir une fenêtre de sélection de fichier
file_path = easygui.fileopenbox(title="Sélectionnez une image", filetypes=["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff"])

if file_path:
    # Récupérer le nom de base du fichier et ajouter "_dxt" avant l'extension
    base_name, _ = os.path.splitext(os.path.basename(file_path))
    downloads_folder = os.path.expanduser("~/Downloads")  # Dossier de téléchargements
    output_image_path = os.path.join(downloads_folder, f"{base_name}_dxt.dds")

    # Fonction pour enlever les pixels d'une couleur spécifique
    def remove_color_pixels(image_path, output_path, color):
        img = imageio.imread(image_path)
        
        # Si l'image est en RGB, ajouter un canal alpha (transparence)
        if img.shape[2] == 3:  # RGB
            img = np.dstack([img, np.ones((img.shape[0], img.shape[1]), dtype=np.uint8) * 255])  # Ajouter un canal alpha complet (opaque)

        # Appliquer une transparence aux pixels similaires à la couleur cible
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                r, g, b, a = img[y, x]  # Récupérer les valeurs des pixels (RGBA)
                if r == color[0] and g == color[1] and b == color[2]:
                    img[y, x] = [0, 0, 0, 0]  # Rendre le pixel transparent

        # Sauvegarder l'image temporaire en PNG avant la conversion
        temp_image_path = output_path.replace('.dds', '_temp.png')
        imageio.imwrite(temp_image_path, img)
        print(f"L'image avec pixels supprimés a été sauvegardée sous : {temp_image_path}")

        # Utiliser Crunch pour convertir l'image en DXT (format DDS)
        subprocess.run(['crunch', '-dxt5', temp_image_path, '-o', output_path], check=True)
        print(f"L'image a été convertie en DXT et sauvegardée sous : {output_path}")

    # Demander à l'utilisateur de sélectionner une couleur
    color = select_color()
    if color:
        # Appeler la fonction pour enlever la couleur spécifiée
        remove_color_pixels(file_path, output_image_path, color)
    else:
        print("Aucune couleur sélectionnée. Le programme a été interrompu.")
