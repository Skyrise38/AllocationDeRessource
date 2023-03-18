import pandas as pd
import itertools

def generate_combinations(nb_eleves):
    solutions = []
    projet = [1, 2, 3,4]
    borne = nb_eleves//3
    nb_projet=0
    for x in range(0, borne+1):
        y = (nb_eleves - 3*x) / 4
        if y.is_integer():
            solutions.append((x, int(y)))
            combinations = list(itertools.combinations(projet, int(x+y)))
            for i in range (len(combinations)):
                combinations_bis= list(itertools.permutations(combinations[i]))
                print("\n",combinations_bis)

  
    print (solutions)

    



generate_combinations(10)


