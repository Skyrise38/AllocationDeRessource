import openpyxl
from openpyxl import load_workbook
import random
import munkres
from munkres import Munkres, print_matrix
from tkinter import * 
from tkinter import messagebox
import tkinter as tk


nb_personnes_par_projet=3
nb_projet=19
nb_choix_projet=3
fichier_excel = "sujets choisis test.xlsx"


#Fonction fenetre graphique
def creation_fenetre_graphique():
    fenetre_graphique=Tk()
    fenetre_graphique.geometry("400x400+568+232")
    fenetre_graphique.rowconfigure(0, weight=1)
    fenetre_graphique.rowconfigure(1, weight=1)
    fenetre_graphique.columnconfigure(0, weight=1)
    fenetre_graphique.columnconfigure(1, weight=1)
    bouton_test=Button(fenetre_graphique, text="Test", command=main)
    bouton_test.grid(row=0, column=0)
    fenetre_graphique.mainloop()

#Fonction verif tableau
def verifier_tableau(fichier_excel,nb_choix_projet):
    wb = load_workbook(fichier_excel)
    feuille = wb.active
    nb_lignes = feuille.max_row
    nb_colonnes = feuille.max_column
    flag=1
    for i in range(2,nb_lignes):
        somme=0
        tab=[]
        for j in range(2,nb_colonnes):
            if feuille.cell(column=j, row=i).value!=None:
                flag_caractere=0
                for caractere in str(feuille.cell(column=j, row=i).value):
                    if caractere.isdigit()==False:
                        print("Cellule {} invalide".format(feuille.cell(column=j, row=i).coordinate))
                        if flag==1:
                            flag=0
                        if flag_caractere==0:
                            flag_caractere=1
                if flag_caractere==1:      
                    break
                if int(feuille.cell(column=j, row=i).value)>nb_choix_projet:
                    print("Cellule {} invalide".format(feuille.cell(column=j, row=i).coordinate))
                    if flag==1:
                        flag=0
                somme+=int(feuille.cell(column=j, row=i).value)
                tab.append(int(feuille.cell(column=j, row=i).value))
        flag_choix=0
        if somme!=nb_choix_projet*(nb_choix_projet+1)/2:
            print("Ligne {} invalide : les choix doivent se situer entre {} et {} une seule fois".format(i,1,nb_choix_projet))
            if flag==1:
                flag=0
            if flag_choix==0:
                flag_choix=1
        if len(tab)!=nb_choix_projet:
            if flag_choix==0:
                print("Ligne {} invalide : les choix doivent se situer entre {} et {} une seule fois".format(i,1,nb_choix_projet))
                if flag==1:
                    flag=0
        for k in range(1,nb_choix_projet+1):
            if k not in tab:
                print("Ligne {} invalide : le nombre de choix doit être de {}".format(i,nb_choix_projet))
                if flag==1:
                    flag=0
    if flag==1:
        print("Tableau valide")
        return True
    else :
        return False



#Fonction création dictionnaire
def creation_dictionnaire(fichier_excel,nb_personnes_par_projet):
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
                for k in range(nb_personnes_par_projet):
                    tab_choix.append(10)
            else :
                for k in range(nb_personnes_par_projet):
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
def main():
    tableau_projet=creation_tableau_projet(nb_projet, nb_personnes_par_projet)
    if verifier_tableau(fichier_excel,nb_choix_projet):
        dico = melange_dictionnaire(creation_dictionnaire(fichier_excel,nb_personnes_par_projet))
        matrice=creation_matrice(dico)
        m = Munkres()

        indexes = m.compute(matrice)
        print(indexes)
        i=0
        for key in dico.keys():
            dico[key]["Numéro projet"]=tableau_projet[indexes[i][1]]
            dico[key]["Choix projet"]=matrice[indexes[i][0]][indexes[i][1]]
            i=i+1
            if dico[key]["Choix projet"]==10:
                print("{} est assigné au projet {} et ce n'est pas son choix".format(dico[key]["Nom"],dico[key]["Numéro projet"]))
            else:
                print("{} est assigné au projet {} et c'est son choix {}".format(dico[key]["Nom"],dico[key]["Numéro projet"],dico[key]["Choix projet"]))
        print ('val=', sum([matrice[k[0]][k[1]] for k in indexes])) 
    
creation_fenetre_graphique()