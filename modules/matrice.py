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
        if null_diag:
            mat[i][i] = 0
    return mat