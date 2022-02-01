from random import randint

def random_int_list(n, bound):
    tab = []
    for i in range(n):
        tab.append(randint(0, bound))
    return tab

def random_matrix(n, bound, null_diag = False, symmetric = False, oriented = False, triangular = False):
    mat = []
    for _ in range(n):
        mat.append(random_int_list(n, bound))
            
    for x in range(n):
        for y in range(n):
            if null_diag and x == y:
                mat [x][y] = 0
            if oriented and mat[x][y] > 0 and x > y:
                y_loc = y
                x_loc = x
                if(randint(0, 10) % 2 == 0):
                    x_loc, y_loc = y_loc, x_loc
                mat[y_loc][x_loc] = 0
            if symmetric:
                mat[y][x] = mat[x][y]
            if triangular and x > y:
                mat[x][y] = 0
    return mat