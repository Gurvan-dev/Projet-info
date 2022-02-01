from random import randint

def random_int_list(n, bound):
    tab = []
    for i in range(n):
        tab.append(randint(0, bound))
    return tab

def random_matrix(n, bound, null_diag = False, symmetric = False, oriented = False, triangular = False):
    mat = []
    for i in range(n):
        mat.append(random_int_list(n, bound))
            
    for x in range(n):
         for y in range(n):
            if null_diag and x == y:
                mat [x][y] = 0
            if oriented and mat[x][y] > 0:
                mat[y][x] = 0
            if symmetric:
                mat[y][x] = mat[x][y]
            if triangular and x > j:
                mat[x][y] = 0
    return mat