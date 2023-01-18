def creation_matrice(eleves):
    matrice=[]
    for key in eleves.keys():
        matrice.apppend(int(eleves[key]["tab_choix"]))
    return matrice