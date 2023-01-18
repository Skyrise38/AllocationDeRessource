def creation_matrice(eleves):
    matrice=[]
    for key in eleves.keys():
        matrice.append(eleves[key]["tab_choix"])
    return matrice