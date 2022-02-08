from random import randint, betavariate

def random_int_list(n, bound, number_generator=(lambda a,b: randint(a, b))):
    tab = []
    for i in range(n):
        tab.append(number_generator(0, bound))
    return tab

def random_matrix(n, bound, null_diag = False, symmetric = False, oriented = False, triangular = False, number_generator=(lambda a,b: randint(a, b))):
    mat = []
    for _ in range(n):
        mat.append(random_int_list(n, bound, number_generator))
            
    for x in range(n):
        for y in range(n):
            if null_diag and x == y:
                mat [x][y] = 0
            if oriented and mat[x][y] > 0 and mat[y][x] > 0: # Si le graph est orienté et qu'on a une valeur non nulle, on va vérifier que la valeur 'réciproque' est également nulle.
                y_loc, x_loc = y, x                          # On a ici un graphe non orienté. On doit 'annuler' une arrête. Pour avoir un graphe réellement aléatoire, on va choisir une des deux arrête au hasard et la supprimer.
                if(randint(0, 10) % 2 == 0):
                    x_loc, y_loc = y_loc, x_loc
                mat[y_loc][x_loc] = 0
            if symmetric:
                mat[y][x] = mat[x][y]
            if triangular and x > y: # On va ici neutraliser le triangle supérieur droit de la matrice.
                mat[x][y] = 0
    return mat