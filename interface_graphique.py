#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:40:25 2023

@author: lorislombard
"""

import tkinter as tk
from tkinter import filedialog

# Créer une fenêtre tkinter
window = tk.Tk()

# Définir la taille de la fenêtre
window.geometry('400x200')

# Définir le titre de la fenêtre
window.title('Sélectionner un fichier Excel')

# Fonction pour sélectionner un fichier Excel
def select_file():
    filename = filedialog.askopenfilename(initialdir='/', title='Sélectionner un fichier', filetypes=[('Fichier Excel', '*.xlsx')])
    print('Le fichier sélectionné est:', filename)

# Fonction pour lancer une fonction pré-définie
def run_function():
    # Remplacer "ma_fonction()" par la fonction que vous souhaitez exécuter
    ma_fonction()

# Bouton pour sélectionner un fichier
btn_select = tk.Button(window, text='Sélectionner un fichier Excel', command=select_file)
btn_select.pack(pady=20)

# Bouton pour lancer une fonction
btn_run = tk.Button(window, text='Lancer la fonction', command=run_function)
btn_run.pack(pady=10)

# Fonction à exécuter
def ma_fonction():
    print('La fonction a été exécutée avec succès!')

# Lancer la boucle principale de la fenêtre
window.mainloop()
