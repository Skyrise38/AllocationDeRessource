#%%

#                         TRIER IMPORT !!!!!!!!!!

import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
import random
import munkres
from munkres import Munkres, print_matrix
from tkinter import * 
from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from itertools import combinations
from copy import copy
import numpy as np

from tkinter import * 
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import time 
from time import strftime
import datetime 
from datetime import datetime, timedelta
from pathlib import Path
import os, shutil
from tkinter.ttk import Progressbar,Treeview
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.colorchooser import askcolor
import random
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
import random
import munkres
from munkres import Munkres, print_matrix
from tkinter import * 
import numpy as np
import os
import pandas as pd
from itertools import combinations
from copy import copy
import numpy as np
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Spinbox
from tkinter import Label
from tkinter import Button
from tkinter import Tk,Toplevel,IntVar,Entry, Frame, Scrollbar
#%%

#                               SUPPRIMER VARIABLES GLOBALES !!!!!
nb_personnes_par_projet=3
#nb_projet=18
#nb_test=10
nb_choix=3
nb_eleves=30
tab_color=["red","blue"]
tab_label=["% Réussite matrice","% Réussite élève"]
# fichier_excel = r"C:\Users\robin\OneDrive\Documents\Projet IESE4 - Allocation de ressources\AllocationDeRessource\attribution sujets.xlsx"
# df= pd.read_excel(fichier_excel,index_col=0)
Contraintes = ["Ensemble","Séparé"]
Ensemble=[]
Separe=[]
Label_contraintes=[]
Bouton_contraintes=[]

    
#%%

def simplifier_dataframe(df):
    df_copy = df.copy()
    df_copy = df_copy.loc[(df==1).any(axis=1)]
    df_copy[df_copy!=1]=10
    indexnames=[]
    l1 = (df_copy.sum(axis=0).to_frame()[0]<=(nb_eleves*10-nb_choix*9)).tolist()
    l2 = (df_copy.sum(axis=0).to_frame()[0]<=(nb_eleves*10-nb_choix*9)).index.tolist()
    for i in range(len(l1)):
        if l1[i]==False:
            indexnames.append(l2[i])
            
    df_copy.drop(indexnames,axis=1,inplace=True)
    return df_copy


#%%
def generate_combinations(projets,nb_eleves):
    solutions = {}
    borne = nb_eleves//3
    compteur=0
    for x in range(0, borne+1):
       y = (nb_eleves - 3*x) / 4
       if y.is_integer():
           combinaisons = []
           #Combinaisons de projets de 3 
           projets_3 = list(combinations(projets,x))
           for i in range(len(projets_3)):
           #Copie du tableau de projets
            tab_temp = copy(projets)       
            #Suppression projets de 3 dans liste de projets
            for j in range(len(projets_3[i])):
                tab_temp.remove(projets_3[i][j])
            #Combinaisons de projets de 4
            projets_4 = list(combinations(tab_temp,int(y)))
            #Ajout des projets de 4 dans projets
            for k in range(len(projets_4)):
                #Ajout des projets de 3 dans la combinaison
                combinaison = list(projets_3[i])
                for l in range(len(projets_4[k])):
                    combinaison.append(projets_4[k][l])
                combinaisons.append(combinaison)
                compteur+=1
            solutions[(x, int(y))]=combinaisons
    return solutions

#%%

def duplication_dataframe(df,combinaisons):
    tab_dataframe=[]
    nb_combinaisons = 0
    progression = 0
    for key in combinaisons.keys():
        nb_combinaisons+=len(combinaisons[key])
    segment = nb_combinaisons//100
    colonnes = df.columns.tolist()
    for key in combinaisons.keys():
        for i in range(0,len(combinaisons[key])):
            df_cour = df.copy()
            compteur = 0
            
            fenetre_accueil.update_idletasks()
            
            for j in range(0,len(colonnes)):
                if str(colonnes[j]) not in combinaisons[key][i]:
                    df_cour = df_cour.drop(colonnes[j],axis=1)
            for x in range(0,key[0]):
                for nb_x in range(0,3):
                    nom_col = combinaisons[key][i][x]
                    df_cour.insert(compteur,int(nom_col),df[int(nom_col)],allow_duplicates=True)
                    compteur+=1
            for y in range(0,key[1]):
                for nb_y in range(0,4):
                    nom_col = combinaisons[key][i][key[0]+y]
                    df_cour.insert(compteur,int(nom_col),df[int(nom_col)],allow_duplicates=True)
                    compteur+=1
            #Mélange lignes / colonnes
            df_cour = df_cour.sample(frac=1)
            df_cour = df_cour.sample(frac=1, axis=1)
            tab_dataframe.append(df_cour)
            progression+=1
            if (progression/segment)%1 == 0:
                progression_bar()
                fenetre_accueil.update_idletasks()
            # Arret à 100 pour faire des tests
            if progression==10000:
                return tab_dataframe
            print(len(tab_dataframe))
    return tab_dataframe

#%%

def progression_bar():
    progression_algo['value']+=0.5
#%%
def conversion_dataframe_matrice(tab):
    tab_matrices = []
    tableau = tab.copy()
    for i in range (len(tab)):
        tab_matrices.append(tableau[i].to_numpy())
    return tab_matrices
             

#%%
#Fonction verification Excel
def verifier_excel(fichier_excel,nb_choix):
    df = pd.read_excel(fichier_excel,index_col=0)
    nb_lignes = df.shape[0]
    nb_colonnes = df.shape[1]
    for i in range(nb_lignes):
        if((int(df.iloc[i].sum())) == nb_choix):
            for j in range(nb_colonnes):
                if ((pd.isnull(df.iloc[i][j]))==False) and (df.iloc[i][j]!=1):
                    print("Ligne {} invalide".format(i)) 
                    return False
        else:
            print("Ligne {} invalide".format(i)) 
            return False
    print("Tableau valide")
    return True
            

#%%

def choix_algo_munkres():
    if var_algo.get()==0:
        return
    bouton_munkres.config(bg="light green",activebackground="light green")
    bouton_guroby.config(bg="white",activebackground="white")
    var_algo.set(0)
    
    global bouton_charger_excel
    global label_fichier
    global path_label
    global bouton_generer
    global bouton_afficher
    global label_nom_excel
    global zone_nom_excel
    global bouton_enregistrer
    global bouton_increment_solution
    global bouton_decrement_solution
    global label_nombre_solutions
    global zone_de_texte
    global label_nb_solutions
    global progression_algo
    
    bouton_charger_excel.destroy()
    label_fichier.destroy()
    path_label.destroy()
    bouton_generer.destroy()
    bouton_afficher.destroy()
    label_nom_excel.destroy()
    zone_nom_excel.destroy()
    bouton_enregistrer.destroy()
    bouton_increment_solution.destroy()
    bouton_decrement_solution.destroy()
    label_nombre_solutions.destroy()
    zone_de_texte.destroy()
    label_nb_solutions.destroy()
    progression_algo.destroy()
    
    bouton_contrainte.destroy()
    nb_max_projets.destroy()
    label_max_projets.destroy()
    
    
    bouton_charger_excel=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Charger excel", font=('Courier', 11,'italic'),command=charger_fichier)
    bouton_charger_excel.grid(column=0,columnspan=4, row=2)
    
    label_fichier = Label(fenetre_accueil,bg="white", text="Fichier chargé :",font=("Courier", 12,"italic"))
    label_fichier.grid(column=0, row=3)
    
    path_label= Label(fenetre_accueil,bg="white", text=fichier_path.get(),font=("Courier", 12,"italic"))
    path_label.grid(column=1,columnspan=3, row=3)
    
    bouton_generer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Generer solution", font=('Courier', 11,'italic'),command=combinaisons_algo)
    bouton_generer.grid(column=0, row=4)
    
    bouton_afficher=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Afficher", font=('Courier', 11,'italic'),command=lambda:affichage_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
    bouton_afficher.grid(column=2, row=4)
    
    bouton_increment_solution=Button(fenetre_accueil, bg="white",activebackground="white", text="Precedent",font=('Courier', 11,'italic'),command=solution_precedente)
    bouton_increment_solution.grid(column=1, row=4)

    bouton_decrement_solution=Button(fenetre_accueil, bg="white",activebackground="white", text="Suivant",font=('Courier', 11,'italic'),command=lambda:solution_suivante(len(succes_tab_dataframes)))
    bouton_decrement_solution.grid(column=3, row=4)
    
    label_nombre_solutions = Label(fenetre_accueil, bg="white", text="Nombre de solutions : ",font=("Courier", 12,"italic"))
    label_nombre_solutions.grid(column=1, row=5)
    zone_de_texte = Entry(fenetre_accueil,bg="light green",justify="center",textvariable=numero_solution,text="")
    zone_de_texte.grid(column=2,row=5)
    label_nb_solutions = Label(fenetre_accueil,bg="white",text="/  0")
    label_nb_solutions.grid(column=3, row=5,sticky=W)
    progression_algo = Progressbar(fenetre_accueil,orient='horizontal',length=300,mode='determinate',value=0)
    progression_algo.grid(column=0, row=5)
    
    label_nom_excel = Label(fenetre_accueil, bg="white", text="Nom du Excel :",font=("Courier", 12,"italic"))
    label_nom_excel.grid(column=0, row=6,sticky=E)
    
    zone_nom_excel = Entry(fenetre_accueil,bg="light green",justify="center",textvariable=nom_excel,text="")
    zone_nom_excel.grid(column=1,columnspan=3,row=6,sticky=W)
    
    bouton_enregistrer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Enregistrer", font=('Courier', 11,'italic'),command=lambda:enregistrer_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
    bouton_enregistrer.grid(column=0,columnspan=4, row=7)
    
    
def choix_algo_guroby():
   if var_algo.get()==1:
       return
   
   global fenetre_accueil
   fenetre_accueil.rowconfigure(8, weight=1)
   fenetre_accueil.rowconfigure(9, weight=1)
   
   global bouton_charger_excel
   global label_fichier
   global path_label
   global bouton_generer
   global bouton_afficher
   global label_nom_excel
   global zone_nom_excel
   global bouton_enregistrer
   bouton_charger_excel.destroy()
   label_fichier.destroy()
   path_label.destroy()
   bouton_generer.destroy()
   bouton_afficher.destroy()
   label_nom_excel.destroy()
   zone_nom_excel.destroy()
   bouton_enregistrer.destroy()
   bouton_increment_solution.destroy()
   bouton_decrement_solution.destroy()
   label_nombre_solutions.destroy()
   zone_de_texte.destroy()
   label_nb_solutions.destroy()
   progression_algo.destroy()
   
   
   bouton_guroby.config(bg="light green",activebackground="light green")
   bouton_munkres.config(bg="white",activebackground="white")
   var_algo.set(1)
   global bouton_contrainte
   bouton_contrainte=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Contrainte", font=('Courier', 11,'italic'),command=fenetre_contraintes)
   bouton_contrainte.grid(column=0, columnspan=4,row=5)
   
   global label_max_projets
   label_max_projets = Label(fenetre_accueil,bg="white", text="Nombre max de projets",font=("Courier", 12,"italic"))
   label_max_projets.grid(column=0, row=2)

   global nb_max_projets
   nb_max_projets = Spinbox(fenetre_accueil,bg="light green",justify="center", from_=1, to=30,font=("Courier", 12,"italic"))
   nb_max_projets.delete(0)
   nb_max_projets.insert(0,"15")
   nb_max_projets.grid(column=1,columnspan=3, row=2)
      
   bouton_charger_excel=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Charger excel", font=('Courier', 11,'italic'),command=charger_fichier)
   bouton_charger_excel.grid(column=0,columnspan=4, row=3)
   
   label_fichier = Label(fenetre_accueil,bg="white", text="Fichier chargé :",font=("Courier", 12,"italic"))
   label_fichier.grid(column=0, row=4)
   
   path_label= Label(fenetre_accueil,bg="white", text=fichier_path.get(),font=("Courier", 12,"italic"))
   path_label.grid(column=1,columnspan=3, row=4)
   
   bouton_generer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Generer solution", font=('Courier', 11,'italic'),command=combinaisons_algo)
   bouton_generer.grid(column=0, row=6)
   
   bouton_afficher=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Afficher", font=('Courier', 11,'italic'),command=lambda:affichage_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
   bouton_afficher.grid(column=2, row=6)
   
   label_nom_excel = Label(fenetre_accueil, bg="white", text="Nom du Excel :",font=("Courier", 12,"italic"))
   label_nom_excel.grid(column=0, row=7,sticky=E)
   
   zone_nom_excel = Entry(fenetre_accueil,bg="light green",justify="center",textvariable=nom_excel,text="")
   zone_nom_excel.grid(column=1,columnspan=3,row=7,sticky=W)

   bouton_enregistrer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Enregistrer", font=('Courier', 11,'italic'),command=lambda:enregistrer_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
   bouton_enregistrer.grid(column=0,columnspan=4, row=8)

#%%
#Test
def resultat_algo(tab_dataframes,tab_matrices):
    tab_matrices_copy = tab_matrices.copy()
    tab_dataframes_copy = tab_dataframes.copy()
    compteur=0
    segment = len(tab_matrices)//100
    progression = 0
    succes_tab_matrices=[]
    succes_tab_dataframes=[]
    succes_indexes=[]
    for i in range(len(tab_matrices)):
            print(i)
            progression+=1
            if (progression/segment)%1==0:
                progression_bar()
                fenetre_accueil.update_idletasks()
            # Arret à 100 pour faire des tests
            if progression==10000:
                return succes_indexes,succes_tab_matrices,succes_tab_dataframes
            fenetre_accueil.update_idletasks()
            m = Munkres()
            temp=tab_matrices_copy[i].copy()
            indexes = m.compute(temp)
            if (sum([tab_matrices[i][k[0]][k[1]] for k in indexes])==30):
                if indexes not in succes_indexes:
                    succes_indexes.append(indexes)
                    succes_tab_matrices.append(tab_matrices_copy[i])
                    succes_tab_dataframes.append(tab_dataframes_copy[i])
                    compteur+=1 
    print("Nombre de succes : {}".format(compteur))
    return succes_indexes,succes_tab_matrices,succes_tab_dataframes

#%%

def solution_suivante(nb_succes):
    global numero_solution
    if int(numero_solution.get())==nb_succes:
        messagebox.showinfo("Erreur","Max solution")
    else:
        numero_solution.set(str(int(numero_solution.get())+1))
        maj_numero_solution(numero_solution.get())
        
def solution_precedente():
    global numero_solution
    global nb_combinaisons
    if int(numero_solution.get())==1:
        messagebox.showinfo("Erreur","Min solution")
    else:
        numero_solution.set(str(int(numero_solution.get())-1))
        maj_numero_solution(numero_solution.get())
#%%

def affichage_resultat(index,dataframe):
     for i in range(len(index)):
        print("{} est assigné au projet {}".format(dataframe.index.tolist()[i],dataframe.columns.tolist()[index[i][1]]))
     
     df_resultat = dataframe.sort_index()
     noms_resultat = df_resultat.index.tolist()
     index_resultat = []
     
     for nom1 in noms_resultat : 
         for j in range(len(dataframe.index.tolist())):
             if nom1==dataframe.index.tolist()[j]:
                 index_resultat.append(index[j])
    
     global fenetre_resultat
     fenetre_resultat = Tk()
     fenetre_resultat.title("Résultat")
     fenetre_resultat.configure(bg="white")
     fenetre_resultat.columnconfigure(0,weight=1)
     fenetre_resultat.rowconfigure(0,weight=1)
     fenetre_resultat.rowconfigure(1, weight=5)
     
     tableau_frame = Frame(fenetre_resultat)
     tableau_frame.grid(column=0, row=1)
     
     titre = Label(fenetre_resultat, bg="white", text="Résultat", font=("Courier",25, "italic", "underline"))
     titre.grid(row=0, column=0)
     
     scrollbar = Scrollbar(tableau_frame)
     scrollbar.pack(side ='right', fill='y')
     
     global tableau
     tableau= Treeview(tableau_frame,yscrollcommand=scrollbar.set )
     tableau.pack(side ="left", expand=1)
     scrollbar.config(command=tableau.yview)
     style = ttk.Style(fenetre_resultat)
     style.configure("Treeview", font=("Courier", 11, "italic"))
     style.configure("Treeview.Heading", font=("Courier", 11, "italic"))
     tableau["columns"] = ("Noms", "N° Projet")
     tableau.column("Noms", anchor='center')
     tableau.column("N° Projet", anchor='center')
     tableau.heading("Noms", text='Noms')
     tableau.heading("N° Projet", text='N° Projet')
     tableau['show'] = 'headings'
     for i in range(len(index)):
         tableau.insert("",'end', values=(df_resultat.index.tolist()[i],df_resultat.columns.tolist()[index_resultat[i][1]]))
     tableau.config(height=len(index))

     fenetre_resultat.mainloop()

#%%
def enregistrer_resultat(index,dataframe):
    index_df = []
    col1 = []
    for i in range(len(index)):
        index_df.append(dataframe.index.tolist()[i])
        col1.append(dataframe.columns.tolist()[index[i][1]])
    df_resultat = pd.DataFrame(data={"N° Projet":col1}, index=index_df)
    df_resultat.sort_index(inplace=True)
    if zone_nom_excel.get()=="":
        df_resultat.to_excel("Resultat.xlsx")
    else : 
        df_resultat.to_excel(zone_nom_excel.get()+".xlsx")
#%%
def fenetre_principale():
    global fenetre_accueil
    fenetre_accueil = Tk()
    fenetre_accueil.geometry("1200x800+360+140")
    fenetre_accueil.configure(bg="white")
    fenetre_accueil.resizable(False,False)
    fenetre_accueil.title("Accueil")
    fenetre_accueil.columnconfigure(0, weight=3)
    fenetre_accueil.columnconfigure(1, weight=1)
    fenetre_accueil.columnconfigure(2, weight=1)
    fenetre_accueil.columnconfigure(3, weight=1)
    fenetre_accueil.rowconfigure(0, weight=2)
    fenetre_accueil.rowconfigure(1, weight=1)
    fenetre_accueil.rowconfigure(2, weight=1)
    fenetre_accueil.rowconfigure(3, weight=1)
    fenetre_accueil.rowconfigure(4, weight=1)
    fenetre_accueil.rowconfigure(5, weight=1)
    fenetre_accueil.rowconfigure(6, weight=1)
    fenetre_accueil.rowconfigure(7, weight=1)
    
    global var_algo
    var_algo = IntVar()
    var_algo.set(0)
    
    global nom_excel
    nom_excel = StringVar()
    nom_excel.set("")
    
    titre = Label(fenetre_accueil, bg="white", text="Affectation de projets", font=("Courier",20,"italic"))
    titre.grid(column=0, columnspan=4, row=0)
    
    label_choix = Label(fenetre_accueil, bg="white", text="Choix de l'algorithme :", font=("Courier",15,"italic"))
    label_choix.grid(column=0, row=1)
    
    global bouton_munkres
    bouton_munkres = Button(fenetre_accueil, bg="light green", activebackground="light green", text="Munkres", font=("Courier",12,"italic"),command=choix_algo_munkres)
    bouton_munkres.grid(column=1, columnspan=2, row=1)
    
    global bouton_guroby
    bouton_guroby = Button(fenetre_accueil, bg="white", activebackground="white", text="Guroby", font=("Courier",12,"italic"),command=choix_algo_guroby)
    bouton_guroby.grid(column=2, columnspan=2, row=1)
    
    global numero_solution
    numero_solution = StringVar()
    numero_solution.set("1")
    
    global fichier_path
    fichier_path = StringVar()
    fichier_path.set("Aucun fichier chargé")
    
    global bouton_charger_excel
    bouton_charger_excel=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Charger excel", font=('Courier', 11,'italic'),command=charger_fichier)
    bouton_charger_excel.grid(column=0,columnspan=4, row=2)
    
    global label_fichier
    label_fichier = Label(fenetre_accueil,bg="white", text="Fichier chargé :",font=("Courier", 12,"italic"))
    label_fichier.grid(column=0, row=3)
    
    global path_label
    path_label= Label(fenetre_accueil,bg="white", text=fichier_path.get(),font=("Courier", 12,"italic"))
    path_label.grid(column=1,columnspan=3, row=3)
    
    global bouton_generer
    bouton_generer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Generer solution", font=('Courier', 11,'italic'),command=combinaisons_algo)
    bouton_generer.grid(column=0, row=4)
    
    global bouton_afficher
    bouton_afficher=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Afficher", font=('Courier', 11,'italic'),command=lambda:affichage_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
    bouton_afficher.grid(column=2, row=4)
    
    global bouton_increment_solution
    bouton_increment_solution=Button(fenetre_accueil, bg="white",activebackground="white", text="Precedent",font=('Courier', 11,'italic'),command=solution_precedente)
    bouton_increment_solution.grid(column=1, row=4)
    
    global bouton_decrement_solution
    bouton_decrement_solution=Button(fenetre_accueil, bg="white",activebackground="white", text="Suivant",font=('Courier', 11,'italic'),command=lambda:solution_suivante(len(succes_tab_dataframes)))
    bouton_decrement_solution.grid(column=3, row=4)
    
    global label_nombre_solutions
    label_nombre_solutions = Label(fenetre_accueil, bg="white", text="Nombre de solutions : ",font=("Courier", 12,"italic"))
    label_nombre_solutions.grid(column=1, row=5)
    global zone_de_texte
    zone_de_texte = Entry(fenetre_accueil,bg="light green",justify="center",textvariable=numero_solution,text="")
    zone_de_texte.grid(column=2,row=5)
    global label_nb_solutions
    label_nb_solutions = Label(fenetre_accueil,bg="white",text="/  0")
    label_nb_solutions.grid(column=3, row=5,sticky=W)
    global progression_algo
    progression_algo = Progressbar(fenetre_accueil,orient='horizontal',length=300,mode='determinate',value=0)
    progression_algo.grid(column=0, row=5)
    
    global label_nom_excel
    label_nom_excel = Label(fenetre_accueil, bg="white", text="Nom du Excel : ",font=("Courier", 12,"italic"))
    label_nom_excel.grid(column=0, row=6,sticky=E)
    
    global zone_nom_excel
    zone_nom_excel = Entry(fenetre_accueil,bg="light green",justify="center",textvariable=nom_excel,text="")
    zone_nom_excel.grid(column=1,columnspan=3,row=6,sticky=W)
    
    global bouton_enregistrer
    bouton_enregistrer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Enregistrer", font=('Courier', 11,'italic'),command=lambda:enregistrer_resultat(succes_index[int(numero_solution.get())-1],succes_tab_dataframes[int(numero_solution.get())-1]))
    bouton_enregistrer.grid(column=0,columnspan=4, row=7)


    fenetre_accueil.mainloop()
#%%
def test():
    print("test")
    
#%%

def charger_fichier():
    global fichier
    fichier = filedialog.askopenfilename()
    if fichier == "":
        fichier_path.set("Aucun fichier chargé")
        path_label.config(font=("Courier", 12,"italic"))
    else:
        fichier_path.set(fichier)
        path_label.config(font=("Courier", 6,"italic"))
    path_label.config(text=fichier_path.get())
#%% 

def fenetre_contraintes():
    global fenetre_contrainte
    fenetre_contrainte = Toplevel(fenetre_accueil)
    fenetre_contrainte.transient(fenetre_accueil)
    fenetre_contrainte.geometry("1400x800")
    fenetre_contrainte.configure(bg="white")
    fenetre_contrainte.title("Contraintes")
    fenetre_contrainte.columnconfigure(0, weight=1)
    fenetre_contrainte.columnconfigure(1, weight=1)
    fenetre_contrainte.columnconfigure(2, weight=1)
    fenetre_contrainte.columnconfigure(3, weight=1)
    fenetre_contrainte.columnconfigure(4, weight=1)
    fenetre_contrainte.columnconfigure(5, weight=1)
    fenetre_contrainte.rowconfigure(0, weight=1)
    fenetre_contrainte.rowconfigure(1, weight=1)
    fenetre_contrainte.rowconfigure(2, weight=1)
    fenetre_contrainte.rowconfigure(3, weight=1)
    fenetre_contrainte.rowconfigure(4, weight=1)
    fenetre_contrainte.rowconfigure(5, weight=1)
    fenetre_contrainte.rowconfigure(6, weight=1)
    fenetre_contrainte.rowconfigure(7, weight=1)
    fenetre_contrainte.rowconfigure(8, weight=1)
    fenetre_contrainte.rowconfigure(9, weight=1)
    
    global contrainte
    contrainte = StringVar(fenetre_contrainte)
    contrainte.set("Ensemble")
    
    global menu_contrainte
    menu_contrainte = OptionMenu(fenetre_contrainte,contrainte, *Contraintes)
    menu_contrainte.config(width=12,bg="white", activebackground="white",highlightthickness=0, font=("Courier", 12,"italic"))
    menu_contrainte["menu"].configure(bg="white",font=("Courier", 12,"italic"))
    menu_contrainte.grid(column=0, row=0)
    
    
    global eleve1
    eleve1 = StringVar(fenetre_contrainte)
    eleve1.set("")
    
    global menu_eleve1
    menu_eleve1 = OptionMenu(fenetre_contrainte,eleve1, *eleves,command=maj_eleves)
    menu_eleve1.config(width=12,bg="white", activebackground="white",highlightthickness=0, font=("Courier", 12,"italic"))
    menu_eleve1["menu"].configure(bg="white",font=("Courier", 12,"italic"))
    menu_eleve1.grid(column=1, row=0)
    
    global eleve2
    eleve2 = StringVar(fenetre_contrainte)
    eleve2.set("")
    
    global menu_eleve2
    menu_eleve2 = OptionMenu(fenetre_contrainte,eleve2, *eleves,command=maj_eleves)
    menu_eleve2.config(width=12,bg="white", activebackground="white",highlightthickness=0, font=("Courier", 12,"italic"))
    menu_eleve2["menu"].configure(bg="white",font=("Courier", 12,"italic"))
    menu_eleve2.grid(column=2, row=0)
    
    global eleve3
    eleve3 = StringVar(fenetre_contrainte)
    eleve3.set("")
    
    global menu_eleve3
    menu_eleve3 = OptionMenu(fenetre_contrainte,eleve3, *eleves,command=maj_eleves)
    menu_eleve3.config(width=12,bg="white", activebackground="white",highlightthickness=0, font=("Courier", 12,"italic"))
    menu_eleve3["menu"].configure(bg="white",font=("Courier", 12,"italic"))
    menu_eleve3.grid(column=3, row=0)
    
    global eleve4
    eleve4 = StringVar(fenetre_contrainte)
    eleve4.set("")
    
    global menu_eleve4
    menu_eleve4 = OptionMenu(fenetre_contrainte,eleve4, *eleves,command=maj_eleves)
    menu_eleve4.config(width=12,bg="white", activebackground="white",highlightthickness=0, font=("Courier", 12,"italic"))
    menu_eleve4["menu"].configure(bg="white",font=("Courier", 12,"italic"))
    menu_eleve4.grid(column=4, row=0)
    
    global bouton_contrainte
    bouton_contrainte = Button(fenetre_contrainte,width=20, bg="white", activebackground="white", text="Valider contrainte", font=("Courier",12,"italic"), command=valider_contrainte)
    bouton_contrainte.grid(column=5, row=0)
    
    titre = Label(fenetre_contrainte, text="Liste des contraintes",bg="white",font=("Courier",18,"italic"))
    titre.grid(column=0, columnspan=6, row=1)
    
    maj_liste_contrainte()
 
#%%

def valider_contrainte():
    tab = []
    if (len(Ensemble)+len(Separe)==8):
        messagebox.showinfo("Erreur","Nombre max de contraintes atteint (8)")
        return
    if (eleve1.get()!=""):
        tab.append(eleve1.get())
    if (eleve2.get()!=""):
        tab.append(eleve2.get())
    if (eleve3.get()!=""):
        tab.append(eleve3.get())
    if (eleve4.get()!=""):
        tab.append(eleve4.get())
    if len(tab)>=2:
        if contrainte.get()=="Ensemble":
            Ensemble.append(tab)
        else:
            Separe.append(tab)
        maj_liste_contrainte()
    else:
        messagebox.showinfo("Erreur","Impossible d'ajouter une telle contrainte")

#%% 

def maj_liste_contrainte():
    for i in range(len(Ensemble)):
        char = str(Ensemble[i])
        exec("global label"+str(i),globals())
        exec("label"+str(i)+" = Label(fenetre_contrainte, text="+'"'+"Ensemble :"+char+'"'+",bg='white',font=('Courier',12,'italic'))",globals())
      #  Label_contraintes.append(label)
        exec("label"+str(i)+".grid(column=0, columnspan=5, row="+str(i)+"+2)",globals())
        exec("global bouton"+str(i),globals())
        exec("bouton"+str(i)+" = Button(fenetre_contrainte, text='Supprimer',bg='white',activebackground='white',font=('Courier',12,'italic'),command=lambda:supprimer_contrainte_ensemble("+str(i)+",bouton"+str(i)+",label"+str(i)+"))",globals())
      #  Bouton_contraintes.append(bouton)
        exec("bouton"+str(i)+".grid(column=4, columnspan=2, row="+str(i)+"+2)",globals())
    for j in range(len(Separe)):
        label = Label(fenetre_contrainte, text="Séparé : "+str(Separe[j]),bg="white",font=("Courier",12,"italic"))
     #   Label_contraintes.append(label)
        label.grid(column=0, columnspan=5, row=j+i+3)
        bouton = Button(fenetre_contrainte, text="Supprimer",bg="white",activebackground="white",font=("Courier",12,"italic"),command=lambda:supprimer_contrainte_separe(j))
      #  Bouton_contraintes.append(bouton)
        bouton.grid(column=4, columnspan=2, row=j+i+3)
    print(Bouton_contraintes)
    print(Label_contraintes)


#%%

def supprimer_contrainte_ensemble(i,bouton,label):
    print("test")
    print(i)
    del Ensemble[i]
    print("test")
    bouton.destroy()
    print("test")
    label.destroy()
    print("test")
    maj_liste_contrainte()


def supprimer_contrainte_separe(j):
    del Separe[j]
    Bouton_contraintes[j].destroy()
    print("test")
    Label_contraintes[j].destroy()
    print("test")
    maj_liste_contrainte()
    

#%%

def maj_eleves(fenetre_contrainte):
    eleves_copy = eleves.copy()
    compteur=0
    for i in range(1,len(eleves)):
        if((eleve1.get()==eleves[i])or(eleve2.get()==eleves[i])or(eleve3.get()==eleves[i])or(eleve4.get()==eleves[i])):
            del eleves_copy[i-compteur]
            compteur+=1  
            
    #MISE A JOUR MENU DEROULANT      
    """ menu = menu_eleve1["menu"]
    menu.delete(0, "end")
    for string in eleves_copy:
        menu.add_command(label=string, command=lambda value=string: fenetre_contrainte.eleve1.set(value))"""
    """ menu_eleve2["menu"]= *eleves
    menu_eleve3["menu"]= *eleves
    menu_eleve4["menu"]= *eleves"""

#%%

def label_numero_solution(nb_succes):
    zone_de_texte.delete(0,"end")
    zone_de_texte.insert(0, "1")
    label_nb_solutions.config(text="/  {}".format(nb_succes))
    
#%%

def maj_numero_solution(val):
    zone_de_texte.delete(0,"end")
    zone_de_texte.insert(0, val)
#%%

def combinaisons_algo():
    
    if fichier_path.get()=="Aucun fichier chargé":
        messagebox.showinfo("Erreur","Veuillez sélectionner un fichier")
        return
    df = pd.read_excel(fichier_path.get(),index_col=0)
    df = simplifier_dataframe(df)

    global projets
    projets = df.columns.tolist()
    
    global solutions
    solutions = generate_combinations(projets,nb_eleves)
    
    global tab_dataframes
    tab_dataframes = duplication_dataframe(df,solutions)
    
    global tab_matrices
    tab_matrices = conversion_dataframe_matrice(tab_dataframes)   

    global succes_index
    global succes_tab_matrices
    global succes_tab_dataframes
    succes_index,succes_tab_matrices,succes_tab_dataframes=resultat_algo(tab_dataframes,tab_matrices)
    
    label_numero_solution(len(succes_tab_dataframes))
#%% 

def fenetre_munkres(nb_eleves):
    
    fenetre_principale()
    
         
    
#%% 

fenetre_munkres(nb_eleves)
#%% 
 
    
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

#%%
#ORDRE : nb_eleves/nb_projet/nb_personnes_par_projet/nb_choix/nb_test
# 50/18/3/3

#Fonction bouton test
def test():
    #test_nb_personnes_par_projet("Nombre de personnes par projet",1,4,1,36,20,3,10,tab_label)
    #test_nb_choix("Nombre de choix par élève",1,4,1,50,18,3,10,tab_label)
    test_nb_eleves("Nombre d'élèves",20,40,5,18,3,3,10,tab_label)
    #test_nb_projet("Nombre de projets",5,10,1,36,4,3,10,tab_label)


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



#Fonction test nombre d'élèves
def test_nb_eleves(nom_variable,borne_inf,borne_supp,pas,nb_projet,nb_personnes_par_projet,nb_choix,nb_test,tab_label):
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

#Fonction test nombre de projet
def test_nb_projet(nom_variable,borne_inf,borne_supp,pas,nb_eleves,nb_personnes_par_projet,nb_choix,nb_test,tab_label):
    if verif_test(borne_inf,borne_supp,pas)==0:
        return
    tab_x,tab_xlabel,tab_y_reussite_matrice,tab_y_reussite_eleves=prepa_test(borne_inf,borne_supp,pas)
    while borne_inf<=borne_supp:
        tab_xlabel.append(borne_inf)
        score_matrice=0
        somme=0
        for x in range(0,nb_test):
            score = 0
            matrice=creation_matrice_aleatoire(nb_eleves,borne_inf,nb_choix,nb_personnes_par_projet)
            m = Munkres()
            indexes = m.compute(matrice)
            for k in indexes:
                if matrice[k[0]][k[1]]==1:
                    score+=1
            somme+=score
            if score==borne_inf:
                score_matrice+=1
        pourcentage_reussite_eleves=somme*100/(nb_test*nb_eleves)
        tab_y_reussite_eleves.append(pourcentage_reussite_eleves)
        pourcentage_reussite_matrice=score_matrice*100/nb_test
        tab_y_reussite_matrice.append(pourcentage_reussite_matrice)
        borne_inf+=pas
    creation_graphique_test_nb_projet(nom_variable,tab_x,tab_y_reussite_matrice,tab_y_reussite_eleves,tab_xlabel,tab_color,nb_personnes_par_projet,nb_eleves,nb_choix,tab_label)

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
def creation_graphique_test_nb_eleves(nom_variable,x,y1,y2,xlabel,tab_color,nb_personnes_par_projet,nb_projet,nb_choix,tab_label):
    ax = creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label)
    ax.set_title("Test du nombre d'élèves avec {} projets, {} élèves par projet et {} choix par élève".format(nb_projet,nb_personnes_par_projet,nb_choix),fontsize=12)
    plt.show()

#Graphique test nombre d'élèves
def creation_graphique_test_nb_projet(nom_variable,x,y1,y2,xlabel,tab_color,nb_personnes_par_projet,nb_eleves,nb_choix,tab_label):
    ax = creation_graphique(nom_variable,x,y1,y2,xlabel,tab_color,tab_label)
    ax.set_title("Test du nombre de projet avec {} élèves, {} élèves par projet et {} choix par élève".format(nb_eleves,nb_personnes_par_projet,nb_choix),fontsize=12)
    plt.show()
