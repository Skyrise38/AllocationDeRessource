import munkres
from munkres import Munkres, print_matrix
import pandas as pd
import time

X = pd.read_excel('attribution sujets.xlsx')
X.iloc[:, 1:] = X.iloc[:, 1:].where(X.iloc[:, 1:] == 1, other=10)
X.drop(X.columns[0], axis=1, inplace=True)

colonnes_dupliquees = []

# Boucler sur toutes les colonnes du DataFrame
for nom_colonne in X.columns:
    # Dupliquer la colonne trois fois et renommer les colonnes dupliquées
    dup1 = X[nom_colonne].copy().rename(str(nom_colonne) + '_dup_1')
    dup2 = X[nom_colonne].copy().rename(str(nom_colonne) + '_dup_2')
    dup3 = X[nom_colonne].copy().rename(str(nom_colonne) + '_dup_3')
    
    # Stocker les colonnes dupliquées dans la liste
    colonnes_dupliquees.extend([dup1, dup2, dup3])

# Concaténer les colonnes dupliquées et les colonnes d'origine
df_concat = pd.concat(colonnes_dupliquees, axis=1)

matrix = df_concat.to_numpy()


""" 
matrix = [[1, 1, 2, 2, 10,10],[1, 1, 10, 10, 2,2],[1, 1, 2, 2, 10,10],[2, 2, 1, 1, 10,10],[1, 1, 2, 2, 10,10],[10 ,10, 1, 1, 2,2]]
"""
temps_debut = time.time()
m = Munkres()

indexes = m.compute(matrix)
print(matrix)
# Fin du temps d'exécution
temps_fin = time.time()

# Temps total d'exécution
temps_execution = temps_fin - temps_debut

print("Le temps d'exécution est de", temps_execution, "secondes.")