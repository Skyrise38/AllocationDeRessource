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
from tkinter import Tk,Toplevel
from main import affichage_resultat
#%%

Contraintes = ["Ensemble","Séparé"]
Ensemble=[]
Separe=[]
Label_contraintes=[]
Bouton_contraintes=[]
fichier_excel = r"C:\Users\robin\OneDrive\Documents\Projet IESE4 - Allocation de ressources\AllocationDeRessource\attribution sujets.xlsx"
df= pd.read_excel(fichier_excel,index_col=0)
nb_choix=3
nb_eleves=30

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
df = simplifier_dataframe(df)
eleves = df.index.tolist()
eleves.insert(0,"")
eleves_copy = eleves.copy()
#%%
def fenetre_principale():
    global fenetre_accueil
    fenetre_accueil = Tk()
    fenetre_accueil.geometry("800x400")
    fenetre_accueil.configure(bg="white")
    fenetre_accueil.title("Accueil")
    fenetre_accueil.columnconfigure(0, weight=1)
    fenetre_accueil.columnconfigure(1, weight=1)
    fenetre_accueil.rowconfigure(0, weight=1)
    fenetre_accueil.rowconfigure(1, weight=1)
    fenetre_accueil.rowconfigure(2, weight=1)
    fenetre_accueil.rowconfigure(3, weight=1)
    fenetre_accueil.rowconfigure(4, weight=1)
    fenetre_accueil.rowconfigure(5, weight=1)
    fenetre_accueil.rowconfigure(6, weight=1)
    
    
    label_max_projets = Label(fenetre_accueil,bg="white", text="Nombre max de projets",font=("Courier", 12,"italic"))
    label_max_projets.grid(column=0, row=0)
    
    label_min_projets = Label(fenetre_accueil,bg="white", text="Nombre min de projets",font=("Courier", 12,"italic"))
    label_min_projets.grid(column=0, row=1)
    
    global nb_max_projets
    nb_max_projets = Spinbox(fenetre_accueil,bg="light blue",justify="center", from_=1, to=10,font=("Courier", 12,"italic"))
    nb_max_projets.delete(0)
    nb_max_projets.insert(0,"4")
    nb_max_projets.grid(column=1, row=0)
    
    global nb_min_projets
    nb_min_projets = Spinbox(fenetre_accueil,bg="light blue",justify="center", from_=1, to=10,font=("Courier", 12,"italic"))
    nb_min_projets.delete(0)
    nb_min_projets.insert(0,"3")
    nb_min_projets.grid(column=1, row=1)
    

    bouton_charger_excel=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Charger excel", font=('Courier', 11,'italic'),command=charger_fichier)
    bouton_charger_excel.grid(column=0,columnspan=2, row=2)
    
    label_fichier = Label(fenetre_accueil,bg="white", text="Fichier chargé :",font=("Courier", 12,"italic"))
    label_fichier.grid(column=0,columnspan=2, row=3)
    
    global path_label
    path_label= Label(fenetre_accueil,bg="white", text="Aucun fichier chargé",font=("Courier", 12,"italic"))
    path_label.grid(column=0,columnspan=2, row=4)
    
    bouton_contrainte=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Contrainte", font=('Courier', 11,'italic'),command=fenetre_contraintes)
    bouton_contrainte.grid(column=0, columnspan=2,row=5)
    
    bouton_generer=Button(fenetre_accueil,bg="white" ,activebackground="white",text="Generer solution", font=('Courier', 11,'italic'),command=lambda:affichage_resultat(succes_index[0],succes_tab_dataframes[0]))
    bouton_generer.grid(column=0, columnspan=2, row=6)
    
    fenetre_accueil.mainloop()
#%%
def test():
    print("test")
    
#%%

def charger_fichier():
   # global fichier_path
    fichier_path = filedialog.askopenfilename()
    if fichier_path == "":
        fichier_path = "Aucun fichier chargé"
        path_label.config(font=("Courier", 12,"italic"))
    else:
        path_label.config(font=("Courier", 6,"italic"))
    path_label.config(text=fichier_path)
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

fenetre_principale()

