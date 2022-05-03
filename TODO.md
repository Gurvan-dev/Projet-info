# PROJET-INFO

## Open_Digraph

- [.] écrire la documentations de "connected_components"
- [.] écrire tests pour "connected_components"
- [.] écrire test pour compose et parallel
- [.] new_id : on peut aussi faire le choix d’incrémenter c dès new_id est
utilisé (dans la méthode, donc), ce qui évite de potentiellement l’oublier.
- [.] add_node : la multiplicité n’est pas prise en compte e.g.
« g.add_node('', {1:3},{}) »
- [.] Doc : c’est bien mais il manque quelques docstrings. Début de typage, c’est une bonne idée, il aurait fallu poursuivre.
- [.] Tests : essayez de les séparer en plusieurs méthodes de tests.
- [.] Utiliser mixins

## Bool_Circ

- [.] Finir TD9: Vérifier K-Map puis question d'après
- [.] TD10 question 4 et 5
- [.] TD12
- [.] On doit penser a supprimer les parents si on fusionne une node et on la transforme en truc primitif

## Possibles bugs & Questions

- [.] La fonctions fusionne node garde-t-elle les inputs outputs ? Comment les gère t-elles ?
- [.] Vérifier que encoder et decodre connectent bien les bons trucs avec les autres bon truc sur le icompose
- [.] Finir typage et docstring pour le reste de bool_circ
- [.] écrire des tests pour bool_circ
  