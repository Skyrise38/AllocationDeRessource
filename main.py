from munkres import Munkres, print_matrix
 
matrix = [[17, 15, 9, 5, 12],
        [16, 16, 10, 5, 10],
        [12, 15, 14, 11, 5],
        [4, 8, 14, 17, 13],
        [13, 9, 8, 12, 17]]
 
m = Munkres()
 
indexes = m.compute(matrix)
 
print_matrix(matrix)
[17, 15,  9,  5, 12]
[16, 16, 10,  5, 10]
[12, 15, 14, 11,  5]
[ 4,  8, 14, 17, 13]
[13,  9,  8, 12, 17]
 
indexes
[(0, 2), (1, 3), (2, 4), (3, 0), (4, 1)]
 
print ('coût=', sum([matrix[i[0]][i[1]] for i in indexes]))
coût= 32