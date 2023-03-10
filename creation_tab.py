# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:20:52 2023

@author: Lombard
"""
import pandas as pd
import random

# définir le nombre d'élèves et de projets

def creation_excel(nb_eleves, nb_projets, nb_choix):
    # créer un dataframe vide avec des noms de colonnes pour les projets
    projets = [f"Project {i:02d}"  for i in range(nb_projets)]
    df = pd.DataFrame(columns=projets)
    
    # ajouter les élèves au dataframe et leur permettre de choisir 3 projets
    eleves = ["Eleve " + str(i+1) for i in range(nb_eleves)]
    for eleve in eleves:
        choix_projets = [0] * nb_projets
        choixs = random.sample(range(nb_projets), nb_choix)
        for choix in choixs:
            choix_projets[choix] = 1
        df.loc[eleve] = choix_projets
       
    # renommer la colonne de l'index
    df.index.name = "N° projet"
    # enregistrer le dataframe dans un fichier Excel
    nom_fichier = "choix_projets.xlsx"
    df.to_excel(nom_fichier)
    return ;
