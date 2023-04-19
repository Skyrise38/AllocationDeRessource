import random

#Fonction mélange dictionnaire
def melange_dictionnaire(d):
    dico=d
    dico_melange={}
    while dico!={}:
        cle=random.choice(tuple(dico.keys()))
        dico_melange[cle]=dico[cle]
        del dico[cle]
    return dico_melange

#Test
print(melange_dictionnaire({"Loris": 10, "Raph":9, "Robin":8,"4": 7, "5":6, "6":5}))