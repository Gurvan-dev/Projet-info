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

## Amélioration possible

- [.] Pour la fonction évaluation, on peut peut être utiliser une liste de fonctions qu'on appelera tour a tour plutôt que plein de if else

## OBLIGATOIRE

- [.] Remove tout les commentaires noté 'REMOVE_NODE' avant rendu

## Possibles bugs & Questions

- [.] La fonctions fusionne node garde-t-elle les inputs outputs ? Comment les gère t-elles ? (En théorie si y'a un input ou un output c'est la merde, donc faudrait mieux pas gérer ?)
- [.] Vérifier que encoder et decodre connectent bien les bons trucs avec les autres bon truc sur le icompose
- [.] Finir typage et docstring pour le reste de bool_circ
- [.] écrire des tests pour bool_circ
- [.] Si on fusionne deux noeuds qui se pointent entre eux, est-ce qu'on obtient une node qui se pointe vers elle même ? (En théorie oui, en pratique : ?)

## Documentations & Autre

- [.] Les documentations des transformations TD 11 ne sont pas les bonnes

## FEEDBACK TD 7

- [.] Dijkstra : je ne pense pas que toutes les copies soient nécessaires, sinon très bien.
( [.] Shortest_path : ça peut être bien de mettre src au début et tgt à la fin de la liste, c’est habituellement comme ça qu’on représente les chemins
(idem longest_path). Très bien sinon.
- [.] tri_topologique : tri_annexe : to_be_removed n’est pas utilisé. On peut faire un peu mieux en terme de complexité en ne cherchant les cofeuilles
que parmi les enfants des cofeuilles précédentes.
  