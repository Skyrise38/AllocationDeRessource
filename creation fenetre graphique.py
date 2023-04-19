from tkinter import * 
from tkinter import messagebox
import tkinter as tk

def creation_fenetre_graphique():
    fenetre_graphique=Tk()
    fenetre_graphique.geometry("400x400+568+232")
    fenetre_graphique.rowconfigure(0, weight=1)
    fenetre_graphique.rowconfigure(1, weight=1)
    fenetre_graphique.columnconfigure(0, weight=1)
    fenetre_graphique.columnconfigure(1, weight=1)
    bouton_test=Button(fenetre_graphique, text="Test", command=test)
    bouton_test.grid(row=0, column=0)

def test():
    print("test")