import openpyxl
from openpyxl import load_workbook
import random
import munkres
from munkres import Munkres, print_matrix
from tkinter import * 
from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np


#nb_personnes_par_projet=2
#nb_projet=18
#nb_choix=3
#nb_eleves=36
#nb_test=10
fichier_excel = "sujets choisis test.xlsx"

    
#Fonction fenetre graphique
def creation_fenetre_graphique():
    fenetre_graphique=Tk()
    fenetre_graphique.geometry("400x400+568+232")
    fenetre_graphique.rowconfigure(0, weight=1)
    fenetre_graphique.rowconfigure(1, weight=1)
    fenetre_graphique.columnconfigure(0, weight=1)
    fenetre_graphique.columnconfigure(1, weight=1)
    bouton_test=Button(fenetre_graphique, text="Test", command=test)
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
        #if somme!=nb_choix_projet*(nb_choix_projet+1)/2:
            #print("Ligne {} invalide : les choix doivent se situer entre {} et {} une seule fois".format(i,1,nb_choix_projet))
            #if flag==1:
            #    flag=0
            #if flag_choix==0:
               # flag_choix=1
        if len(tab)!=nb_choix_projet:
            if flag_choix==0:
                print("Ligne {} invalide : les choix doivent se situer entre {} et {} une seule fois".format(i,1,nb_choix_projet))
                if flag==1:
                    flag=0
        #for k in range(1,nb_choix_projet+1):
            #if k not in tab:
               # print("Ligne {} invalide : le nombre de choix doit être de {}".format(i,nb_choix_projet))
               # if flag==1:
                    #flag=0
    if flag==1:
        #print("Tableau valide")
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
    tab=[]
    for i in range(100):
        tableau_projet=creation_tableau_projet(nb_projet, nb_personnes_par_projet)
        if verifier_tableau(fichier_excel,nb_choix_projet):
            dico = melange_dictionnaire(creation_dictionnaire(fichier_excel,nb_personnes_par_projet))
            matrice=creation_matrice(dico)
            m = Munkres()
            indexes = m.compute(matrice)
            #print(indexes)
            i=0
            for key in dico.keys():
                dico[key]["Numéro projet"]=tableau_projet[indexes[i][1]]
                dico[key]["Choix projet"]=matrice[indexes[i][0]][indexes[i][1]]
                i=i+1
                #if dico[key]["Choix projet"]==10:
                    #print("{} est assigné au projet {} et ce n'est pas son choix".format(dico[key]["Nom"],dico[key]["Numéro projet"]))
                #else:
                    #print("{} est assigné au projet {} et c'est son choix {}".format(dico[key]["Nom"],dico[key]["Numéro projet"],dico[key]["Choix projet"]))
            #print ('val=', sum([matrice[k[0]][k[1]] for k in indexes])) 
            tab.append(sum([matrice[k[0]][k[1]] for k in indexes]))
    print(tab)


def creation_matrice_aleatoire(nb_eleves,nb_projet,nb_choix,nb_personnes_par_projet):
    matrice=[None]*nb_eleves

    for i in range (nb_eleves):
        nb_changement=0
        matrice[i]=[None]*nb_projet*nb_personnes_par_projet
        for j in range (nb_projet*nb_personnes_par_projet):
            matrice[i][j]=10
        while (nb_changement<nb_choix):
            var=random.randint(0,nb_projet-1)
            if (matrice [i][var*nb_personnes_par_projet]==10):
                for k in range(nb_personnes_par_projet):
                    matrice [i][var*nb_personnes_par_projet+k]=1
                nb_changement+=1
        
    
    return matrice


tab_color=["red","blue"]
tab_label=["% Réussites matrice","% Réussite élève"]

#ORDRE : nb_eleves/nb_projet/nb_personnes_par_projet/nb_choix/nb_test
# 50/18/3/3

#Fonction bouton test
def test():
    #test_nb_personnes_par_projet("Nombre de personnes par projet",1,4,1,36,20,3,10,tab_label)
    test_nb_choix("Nombre de choix par élève",1,4,1,50,18,3,10,tab_label)
    test_nb_eleves("Nombre d'élèves",30,50,5,18,3,3,10,tab_label)


#Fonction verification test
def verif_test(borne_inf,borne_supp,pas):
    if borne_inf>borne_supp:
        return 0
    if pas<=0:
        return 0
    return 1

#Fonction préparation test
def prepa_test(borne_inf,borne_supp,pas):
    borne_inf_copie=borne_inf
    tab_x=[]
    tab_xlabel=[]
    tab_y_reussite_matrice=[]
    tab_y_reussite_eleves=[]
    i=1
    while borne_inf_copie<=borne_supp:
        tab_x.append(i)
        i+=1
        borne_inf_copie+=pas
    return tab_x,tab_xlabel,tab_y_reussite_matrice,tab_y_reussite_eleves

#Fonction création graphique
def creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label):
    y=[y1,y2]
    width = 0.2
    x_float=[]
    x_float2=[]
    xticks=[]
    tab_x=[]
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    for k in range(len(x)):
        xticks.append(x[k]+width/2)
        x_float.append(float(x[k]))
        x_float2.append(float(x[k])+width)
    tab_x.append(x_float)
    tab_x.append(x_float2)
    for i in range(2):
        bar = ax.bar(tab_x[i], y[i], width,color=tab_color[i],label=tab_label[i])
        ax.bar_label(bar, padding=1,fmt="%d")
    ax.set_xticks(xticks,xlabel)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 0),edgecolor="white")
    ax.set_xlabel("{}".format(nom_variable))
    ax.set_ylabel('Taux de réussite (%)')
    fig.tight_layout()
    return ax

#Fonction test nombre de choix des élèves
def test_nb_choix(nom_variable,borne_inf,borne_supp,pas,nb_eleves,nb_projet,nb_personnes_par_projet,nb_test,tab_label):
    if verif_test(borne_inf,borne_supp,pas)==0:
        return
    tab_x,tab_xlabel,tab_y_reussite_matrice,tab_y_reussite_eleves=prepa_test(borne_inf,borne_supp,pas)
    while borne_inf<=borne_supp:
        tab_xlabel.append(borne_inf)
        score_matrice=0
        somme=0
        for x in range(0,nb_test):
            score = 0
            matrice=creation_matrice_aleatoire(nb_eleves,nb_projet,borne_inf,nb_personnes_par_projet)
            m = Munkres()
            indexes = m.compute(matrice)
            for k in indexes:
                if matrice[k[0]][k[1]]==1:
                    score+=1
            somme+=score
            if score==nb_eleves:
                score_matrice+=1
        pourcentage_reussite_eleves=somme*100/(nb_test*nb_eleves)
        tab_y_reussite_eleves.append(pourcentage_reussite_eleves)
        pourcentage_reussite_matrice=score_matrice*100/nb_test
        tab_y_reussite_matrice.append(pourcentage_reussite_matrice)
        borne_inf+=pas
    creation_graphique_test_nb_choix(nom_variable,tab_x,tab_y_reussite_matrice,tab_y_reussite_eleves,tab_xlabel,tab_color,nb_eleves,nb_projet,nb_personnes_par_projet,tab_label)


#Fonction test nombre de personnes par projet
def test_nb_personnes_par_projet(nom_variable,borne_inf,borne_supp,pas,nb_eleves,nb_projet,nb_choix,nb_test,tab_label):
    if verif_test(borne_inf,borne_supp,pas)==0:
        return
    tab_x,tab_xlabel,tab_y_reussite_matrice,tab_y_reussite_eleves=prepa_test(borne_inf,borne_supp,pas)
    while borne_inf<=borne_supp:
        tab_xlabel.append(borne_inf)
        score_matrice=0
        somme=0
        for x in range(0,nb_test):
            score = 0
            matrice=creation_matrice_aleatoire(nb_eleves,nb_projet,nb_choix,borne_inf)
            m = Munkres()
            indexes = m.compute(matrice)
            for k in indexes:
                if matrice[k[0]][k[1]]==1:
                    score+=1
            somme+=score
            if score==nb_eleves:
                score_matrice+=1
        pourcentage_reussite_eleves=somme*100/(nb_test*nb_eleves)
        tab_y_reussite_eleves.append(pourcentage_reussite_eleves)
        pourcentage_reussite_matrice=score_matrice*100/nb_test
        tab_y_reussite_matrice.append(pourcentage_reussite_matrice)
        borne_inf+=pas
    creation_graphique_test_nb_personnes_par_projet(nom_variable,tab_x,tab_y_reussite_matrice,tab_y_reussite_eleves,tab_xlabel,tab_color,nb_eleves,nb_projet,nb_choix,tab_label)



#Fonction test nombre d'élèves'
def test_nb_eleves(nom_variable,borne_inf,borne_supp,pas,nb_personnes_par_projet,nb_projet,nb_choix,nb_test,tab_label):
    if verif_test(borne_inf,borne_supp,pas)==0:
        return
    tab_x,tab_xlabel,tab_y_reussite_matrice,tab_y_reussite_eleves=prepa_test(borne_inf,borne_supp,pas)
    while borne_inf<=borne_supp:
        tab_xlabel.append(borne_inf)
        score_matrice=0
        somme=0
        for x in range(0,nb_test):
            score = 0
            matrice=creation_matrice_aleatoire(borne_inf,nb_projet,nb_choix,nb_personnes_par_projet)
            m = Munkres()
            indexes = m.compute(matrice)
            for k in indexes:
                if matrice[k[0]][k[1]]==1:
                    score+=1
            somme+=score
            if score==borne_inf:
                score_matrice+=1
        pourcentage_reussite_eleves=somme*100/(nb_test*borne_inf)
        tab_y_reussite_eleves.append(pourcentage_reussite_eleves)
        pourcentage_reussite_matrice=score_matrice*100/nb_test
        tab_y_reussite_matrice.append(pourcentage_reussite_matrice)
        borne_inf+=pas
    creation_graphique_test_nb_eleves(nom_variable,tab_x,tab_y_reussite_matrice,tab_y_reussite_eleves,tab_xlabel,tab_color,nb_personnes_par_projet,nb_projet,nb_choix,tab_label)

#Graphique test nombre de personnes par projet
def creation_graphique_test_nb_personnes_par_projet(nom_variable,x,y1,y2,xlabel,tab_color,nb_eleves,nb_projet,nb_choix,tab_label):
    ax = creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label)
    ax.set_title("Test du nombre d'élèves par projet avec {} élèves, {} projets et {} choix par élève".format(nb_eleves,nb_projet,nb_choix),fontsize=12)
    plt.show()

#Graphique test nombre de choix par élèves
def creation_graphique_test_nb_choix(nom_variable,x,y1,y2,xlabel,tab_color,nb_eleves,nb_projet,nb_personnes_par_projet,tab_label):
    ax = creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label)
    ax.set_title('Test du nombre de choix par élèves avec {} élèves, {} projets et {} élèves par projet'.format(nb_eleves,nb_projet,nb_personnes_par_projet),fontsize=12)
    plt.show()

#Graphique test nombre d'élèves
def creation_graphique_test_nb_eleves(nom_variable,x,y1,y2,xlabel,tab_color,nb_eleves,nb_projet,nb_personnes_par_projet,tab_label):
    ax = creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label)
    ax.set_title("Test du nombre d'élèves avec {} élèves, {} projets et {} élèves par projet".format(nb_eleves,nb_projet,nb_personnes_par_projet),fontsize=12)
    plt.show()



creation_fenetre_graphique()