import munkres
from munkres import Munkres, print_matrix

matrix = [[1, 1, 2, 2, 10,10],[1, 1, 10, 10, 2,2],[1, 1, 2, 2, 10,10],[2, 2, 1, 1, 10,10],[1, 1, 2, 2, 10,10],[10 ,10, 1, 1, 2,2]]

m = Munkres()

indexes = m.compute(matrix)

print_matrix(matrix)

print(indexes)
print(indexes[0][0])

print ('coût=', sum([matrix[i[0]][i[1]] for i in indexes]))
