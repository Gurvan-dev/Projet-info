# PROJET-INFO

## Open_Digraph

- [.] écrire la documentations de "connected_components"
- [.] écrire tests pour "connected_components"
- [.] écrire test pour compose et parallel
- [.] new_id : on peut aussi faire le choix d’incrémenter c dès new_id est
utilisé (dans la méthode, donc), ce qui évite de potentiellement l’oublier.
- [.] add_node : la multiplicité n’est pas prise en compte e.g.
« g.add_node('', {1:3},{}) »
- [.] is_well_formed : pour inputs, il faut renvoyer false si nb de parents >0 (et pas >1). Il faut également vérifier la multiplicité de l’unique fils de l’input. Idem outputs. Ce qui est fait pour les enfants de j doit être fait pour ses parents aussi.
- [.] Doc : c’est bien mais il manque quelques docstrings. Début de typage, c’est une bonne idée, il aurait fallu poursuivre.
-[.] Tests : essayez de les séparer en plusieurs méthodes de tests.
- [.] Utiliser mixins