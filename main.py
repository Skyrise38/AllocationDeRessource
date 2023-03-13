
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 13:47:54 2023

@author: Lombard
"""


import pandas as pd
import gurobipy as gp
import numpy as np
from gurobipy import GRB
import creation_tab as fct


MAX_STUDENTS_PER_PROJECT = 4
MIN_STUDENTS_PER_PROJECT = 3

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
######################################    Fonctions   #######################################################################

def solve(max_projects):
    # initialize the model object
    m = gp.Model(f"project_assignment_{max_projects}")
    
    assign = m.addVars(permutations, vtype=GRB.BINARY, name="assign")
    use_project = m.addVars(projects, vtype=GRB.BINARY, name="use_project")

    # each student has one and only one project group
    m.addConstrs(
        (assign.sum(student, "*") == 1 for student in students),
        name="EachStudentAssignedToOneProject"
    )

    # projects can't exceed the maximum number of students
    m.addConstrs(
        (assign.sum("*", project) <= MAX_STUDENTS_PER_PROJECT for project in projects),
        name="LimitGroupSize"
    )

    # projects must be considered 'in use' if any students are assigned
    m.addConstrs(
        (use_project[project] >= assign[(student, project)] for student in students for project in projects),
        name="ProjectMustBeInUseIfAnyStudentsAssigned"
    )

    # don't exceed max number of projects
    m.addConstr(use_project.sum() <= max_projects, name="MaxProjects")

    # if any students are assigned to a project, the project must have at least 2 students
    m.addConstrs(
        (assign.sum("*", project) >= use_project[project] * MIN_STUDENTS_PER_PROJECT for project in projects),
        name="ProjectsInUseMustHaveAtLeastTwoStudents"
    )

    # put students together who both indicated the other
    for student1, student2 in together:
        m.addConstrs(
            (assign[(student1, project)] == assign[(student2, project)] for project in projects),
            name=f"PairStudents[{(student1, student1)}]"
        )
    
    # keep students apart who contraindicated another
    for student1, student2 in apart:
        m.addConstrs(
            (
                (assign[(student1, project)] + assign[(student2, project)]
            ) <= 1 for project in projects),
            name=f"ApartStudents[{(student1, student1)}]"
        )

    # set the objective function to be minimized
    m.setObjective(
        (ratings.prod(assign) - 1)**2,
        sense=GRB.MINIMIZE,
    )

    m.optimize()
    return m, assign

def get_results(assign):
    """ Take the dict of results and turn it into useful DataFrames """
    
    # create df with impossible placeholder
    assign_df = pd.DataFrame(-1, index=students, columns=projects)

    # fill in the decision variable results
    for (i, j), x_ij in assign.items():
        assign_df.loc[i, j] = int(x_ij.X)

    # sanity check that none were missed
    assert ((assign_df == 0) | (assign_df == 1)).all().all()
    
    # count how many students got their nth choice
    choices = (assign_df * rank_df).values.ravel()
    choices = choices[choices > 0]
    n_ranks = pd.Series(choices).value_counts().rename(index=lambda x: f"choice {x}")

    # count up how big the group sizes are
    group_sizes = assign_df.sum(axis="rows").sort_values(ascending=False).rename("n").sort_values(ascending=False)
    
    return assign_df, n_ranks, group_sizes




#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
######################################    MAIN    #######################################################################


###### Test pour nb choix allant de 1 à 10

nb_eleves=40
nb_projets=15
nb_matrice_alea=100

for i in range(1,10):
    nb_choix =i
    tab_res=[]
    
    fct.creation_excel(nb_eleves, nb_projets, nb_choix)
    
    #########     Chargement des données   ############
    
    Xdf = pd.read_excel("choix_projets.xlsx")
    # Xdf=Xdf.replace(r'^\s*$',10,regex=True) si tableau vide avec des 1
    Xdf=Xdf.replace(0,10,regex=True)
    Xdf = Xdf.fillna(10)
    Xdf.index=Xdf["N° projet"].tolist()
    
    students = Xdf["N° projet"].tolist()
    Xdf=Xdf.drop("N° projet", axis=1)
    
    i=0;
    nb_succes=0;
    
    while (i<nb_matrice_alea):
        i+=1;
        #########     Mélange des lignes du dataframe         ############
        
        #Xdf=Xdf.sample(frac=1)
        
        
        #########     Mélange de l'ordre des colonnes du DF   ############
        
        #Xdf = Xdf.sample(frac=1, axis=1)
        
        
        #########     Changement des choix des élèves         ############
        
        Xdf = Xdf.apply(np.random.permutation)
        
        #########     Nombre de projets et d'élèves         ############
        
        #I = Xdf.shape[0] # Nombre d'élèves
        #J = Xdf.shape[1] # Nombre de projets
        
        #########     Création du tableau avec le numéro des projets         ############
    
        projects = Xdf.columns.tolist()
        
        
        
        rank_df =Xdf
        
        #########     Liste des élèves ensemble        ############
        
        # Example : together = [("Student 01", "Student 13"), ("Student 05", "Student 06")]
        
        together = [
        
        ]
        
        #########     Liste des élèves à séparer        ############
        
        apart = [
        
        ]
        
        permutations, ratings = gp.multidict({
            (i, j): rank_df.loc[i, j]
            for i in students
            for j in projects
        })
        
        #permutations[:40]
        
        
        #ratings.sum("*", "Project 00")
        #ratings.sum("*", "Project 01")
        
        m, assign = solve(max_projects=15)
        assign_df, n_ranks, group_sizes = get_results(assign)
       
        if (n_ranks[0]==len(students)):
            nb_succes+=1;
            
    tab_res.append(nb_succes/nb_matrice_alea)




###### Test pour nb eleves allant de 20 à 60

nb_choix=3
nb_projets=15
nb_matrice_alea=100

for i in range(20,60,5):
    nb_eleves =i
    tab_res=[]
    
    fct.creation_excel(nb_eleves, nb_projets, nb_choix)
    
    #########     Chargement des données   ############
    
    Xdf = pd.read_excel("choix_projets.xlsx")
    # Xdf=Xdf.replace(r'^\s*$',10,regex=True) si tableau vide avec des 1
    Xdf=Xdf.replace(0,10,regex=True)
    Xdf = Xdf.fillna(10)
    Xdf.index=Xdf["N° projet"].tolist()
    
    students = Xdf["N° projet"].tolist()
    Xdf=Xdf.drop("N° projet", axis=1)
    
    i=0;
    nb_succes=0;
    
    while (i<nb_matrice_alea):
        i+=1;
        #########     Mélange des lignes du dataframe         ############
        
        #Xdf=Xdf.sample(frac=1)
        
        
        #########     Mélange de l'ordre des colonnes du DF   ############
        
        #Xdf = Xdf.sample(frac=1, axis=1)
        
        
        #########     Changement des choix des élèves         ############
        
        Xdf = Xdf.apply(np.random.permutation)
        
        #########     Nombre de projets et d'élèves         ############
        
        #I = Xdf.shape[0] # Nombre d'élèves
        #J = Xdf.shape[1] # Nombre de projets
        
        #########     Création du tableau avec le numéro des projets         ############
    
        projects = Xdf.columns.tolist()
        
        
        
        rank_df =Xdf
        
        #########     Liste des élèves ensemble        ############
        
        # Example : together = [("Student 01", "Student 13"), ("Student 05", "Student 06")]
        
        together = [
        
        ]
        
        #########     Liste des élèves à séparer        ############
        
        apart = [
        
        ]
        
        permutations, ratings = gp.multidict({
            (i, j): rank_df.loc[i, j]
            for i in students
            for j in projects
        })
        
        #permutations[:40]
        
        
        #ratings.sum("*", "Project 00")
        #ratings.sum("*", "Project 01")
        
        m, assign = solve(max_projects=15)
        assign_df, n_ranks, group_sizes = get_results(assign)
       
        if (n_ranks[0]==len(students)):
            nb_succes+=1;
            
    tab_res.append(nb_succes/nb_matrice_alea)


###### Test pour nb projets allant de 10 à 30

nb_choix=3
nb_eleves=40
nb_matrice_alea=100

for i in range(10,30,2):
    nb_projets =i
    tab_res=[]
    
    fct.creation_excel(nb_eleves, nb_projets, nb_choix)
    
    #########     Chargement des données   ############
    
    Xdf = pd.read_excel("choix_projets.xlsx")
    # Xdf=Xdf.replace(r'^\s*$',10,regex=True) si tableau vide avec des 1
    Xdf=Xdf.replace(0,10,regex=True)
    Xdf = Xdf.fillna(10)
    Xdf.index=Xdf["N° projet"].tolist()
    
    students = Xdf["N° projet"].tolist()
    Xdf=Xdf.drop("N° projet", axis=1)
    
    i=0;
    nb_succes=0;
    
    while (i<nb_matrice_alea):
        i+=1;
        #########     Mélange des lignes du dataframe         ############
        
        #Xdf=Xdf.sample(frac=1)
        
        
        #########     Mélange de l'ordre des colonnes du DF   ############
        
        #Xdf = Xdf.sample(frac=1, axis=1)
        
        
        #########     Changement des choix des élèves         ############
        
        Xdf = Xdf.apply(np.random.permutation)
        
        #########     Nombre de projets et d'élèves         ############
        
        #I = Xdf.shape[0] # Nombre d'élèves
        #J = Xdf.shape[1] # Nombre de projets
        
        #########     Création du tableau avec le numéro des projets         ############
    
        projects = Xdf.columns.tolist()
        
        
        
        rank_df =Xdf
        
        #########     Liste des élèves ensemble        ############
        
        # Example : together = [("Student 01", "Student 13"), ("Student 05", "Student 06")]
        
        together = [
        
        ]
        
        #########     Liste des élèves à séparer        ############
        
        apart = [
        
        ]
        
        permutations, ratings = gp.multidict({
            (i, j): rank_df.loc[i, j]
            for i in students
            for j in projects
        })
        
        #permutations[:40]
        
        
        #ratings.sum("*", "Project 00")
        #ratings.sum("*", "Project 01")
        
        m, assign = solve(max_projects=15)
        assign_df, n_ranks, group_sizes = get_results(assign)
       
        if (n_ranks[0]==len(students)):
            nb_succes+=1;
            
    tab_res.append(nb_succes/nb_matrice_alea)



'''
# Générer un fichier Excel à partir du dataframe
assign_df.to_excel('result.xlsx', index=1)
assign_df
n_ranks
group_sizes
'''



# Affichage des résultats
'''for eleve in assign_df.index:
    projet = assign_df.loc[eleve][assign_df.loc[eleve] == 1].index[0]
    print(f"{eleve} est assigné au {projet}")
'''
