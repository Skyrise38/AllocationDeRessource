import random

def creation_matrice_aleatoire(nb_eleve,nb_projet):
    matrice=[None]*nb_eleve

    for i in range (nb_eleve):
        nb_changement=0
        matrice[i]=[None]*nb_projet
        for j in range (nb_projet):
            matrice[i][j]=10
        while (nb_changement<3):
            var=random.randint(0,17)
            if (matrice [i][var]==10):
                matrice [i][var]=1
                nb_changement+=1
        
    
    return matrice

matrice = creation_matrice_aleatoire(36,18)
for i in range (35):
        print(matrice[i])

