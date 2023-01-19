import openpyxl
from openpyxl import load_workbook
import random
import munkres
from munkres import Munkres, print_matrix


nb_personnes_par_projet=2
nb_projet=18

#Fonction création dictionnaire
def creation_dictionnaire(fichier_excel,nb_personnes):
    wb = load_workbook(fichier_excel)
    feuille = wb.active
    nb_lignes = feuille.max_row
    nb_colonnes = feuille.max_column
    eleves={}
    tab_valeurs = ["1","2","3"]
    for i in range(2,nb_lignes):
        tab_choix = []
        for j in range(2,nb_colonnes):
            k=0
            if (str(feuille.cell(column=j, row=i).value)) not in tab_valeurs:
                for k in range(nb_personnes):
                    tab_choix.append(10)
            else :
                for k in range(nb_personnes):
                    tab_choix.append(feuille.cell(column=j, row=i).value)
        eleves[i]={}
        eleves[i]["Nom"]=feuille.cell(column=1, row=i).value
        eleves[i]["tab_choix"]=tab_choix
        eleves[i]["Numéro projet"]=0
    return eleves

#Fonction création matrice
def creation_matrice(eleves):
    matrice=[]
    for key in eleves.keys():
        matrice.append(eleves[key]["tab_choix"])
    return matrice

#Fonction mélange dictionnaire
def melange_dictionnaire(d):
    dico=d
    dico_melange={}
    while dico!={}:
        cle=random.choice(tuple(dico.keys()))
        dico_melange[cle]=dico[cle]
        del dico[cle]
    return dico_melange

#Fonction création tableau projet
def creation_tableau_projet(nb_projet,nb_personnes):
    tab=[]
    for i in range(1,nb_projet+1):
        j=0
        for j in range(nb_personnes):
            tab.append(i)
    return tab



#Test
dico = melange_dictionnaire(creation_dictionnaire("sujets choisis test.xlsx",nb_personnes_par_projet))
matrice=creation_matrice(dico)
tableau_projet=creation_tableau_projet(nb_projet, nb_personnes_par_projet)
print(tableau_projet)
m = Munkres()

indexes = m.compute(matrice)
print(dico)
print(indexes)
i=0
for key in dico.keys():
    dico[key]["Numéro projet"]=tableau_projet[indexes[i][1]]
    dico[key]["Choix projet"]=matrice[indexes[i][0]][indexes[i][1]]
    i=i+1
    print("{} est assigné au projet {} et c'est son choix {}".format(dico[key]["Nom"],dico[key]["Numéro projet"],dico[key]["Choix projet"]))
print ('val=', sum([matrice[k[0]][k[1]] for k in indexes])) 