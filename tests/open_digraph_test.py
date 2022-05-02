import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)
        n0.add_children_id(3, 1)
        self.assertEqual(n0.children, {1: 1, 3 : 1})

    def test_init_open_digraph(self):
        o = open_digraph([0, 1, 2, 7], [0], [])
        self.assertEqual(o.inputs, [0, 1, 2, 7])
        self.assertEqual(o.outputs, [0])
        self.assertEqual(o.nodes, {node.id: node for node in []})

        o2 = o.copy()

        o2.inputs = [0, 1, 2, 3]
        o2.outputs = [2]
        o2.nodes = {node.id : node for node in [node(1, 'i', {}, {1: 1})]}

        self.assertNotEqual(o.inputs, o2.inputs)
        self.assertNotEqual(o.outputs, o2.outputs)
        self.assertNotEqual(o.nodes, o2.nodes)
        self.assertEqual([], o.get_nodes())

        o2.add_node()
        self.assertEqual(o2.nodes[1], node(1, '', {}, {}))

        # Tests TD2

        # Exercice 1

        n1 = node(1, 'i', {1:2, 2:3, 3:1}, {1: 1, 2:4, 3:8})
        n2 = node(2, 'j', {1:5, 2:1, 3:2}, {1: 2, 2:2, 3:5})
        n1.remove_parent_once(2)
        n2.remove_parent_once(2)

        self.assertEqual(n1.get_parents_ids(), {1:2, 2:2, 3:1})
        self.assertEqual(n2.get_parents_ids(), {1:5, 3:2})

        n1.remove_child_once(1)
        n2.remove_child_once(3)

        self.assertEqual(n1.get_children_ids(), {2:4, 3:8})
        self.assertEqual(n2.get_children_ids(), {1: 2, 2:2, 3:4})

        n1.remove_parent_id(2)
        n2.remove_parent_id(3)

        self.assertEqual(n1.get_parents_ids(), {1:2, 3:1})
        self.assertEqual(n2.get_parents_ids(), {1:5})

        n1.remove_child_id(3)
        n2.remove_child_id(1)

        self.assertEqual(n1.get_children_ids(), {2:4})
        self.assertEqual(n2.get_children_ids(), {2:2, 3:4})

        # Exercice 2

            # Tests fonctions simples

        n1 = node(1, 'i', {2:3}, {2:4})
        n2 = node(2, 'j', {1:4}, {1: 3})
        o3 = o2.copy()
        o3.outputs = [1,2]
        o3.nodes = {node.id : node for node in [n1, n2]}
        o3.remove_edge(1, 2)

        self.assertEqual(o3.get_node_by_id(1).get_parents_ids(), {2: 3})
        self.assertEqual(o3.get_node_by_id(1).get_children_ids(), {2: 3})
        self.assertEqual(o3.get_node_by_id(2).get_parents_ids(), {1:3})
        self.assertEqual(o3.get_node_by_id(2).get_children_ids(), {1: 3})

        o3.remove_parallel_edge(1, 2)
        
        self.assertEqual(o3.get_node_by_id(1).get_parents_ids(), {2: 3})
        self.assertEqual(o3.get_node_by_id(1).get_children_ids(), {})

        o3.remove_node_by_id(2)

        self.assertEqual(o3.get_nodes(), [n1])

            # Tests fonctions multiples

        o3 = open_digraph.empty()
        o3.add_node('i')
        o3.add_node('j', {1}, {1})
        o3.add_node('k', {2}, {1})
        o3.remove_edges([(1, 2), (2, 3)])


        self.assertEqual(o3.get_node_by_id(1).get_parents_ids(), {2:1, 3:1})
        self.assertEqual(o3.get_node_by_id(1).get_children_ids(), {})
        self.assertEqual(o3.get_node_by_id(2).get_parents_ids(), {})
        self.assertEqual(o3.get_node_by_id(2).get_children_ids(), {1:1})

        o4 = open_digraph.empty()
        self.assertTrue(o4.is_well_formed())    # Un graph vide devrait être bien formé 
        
        o4.add_node()
        o4.add_input_node(1)
        with self.assertRaises(Exception):
            o4.add_input_node(2)
        o4.add_output_node(1) 

        o5 = o4.copy()
        self.assertTrue(o5.is_well_formed())    # o5 est le graphe le plus simple qui est bien formé, avec un input, un output et un seule node entre les deux.

        o4.add_node()
        o4.add_edge(4, 3)

        self.assertFalse(o4.is_well_formed())   # Le graph a un output avec plusieurs parents, et est donc mal formé.

        o5.add_node()
        o5.add_node()
        o5.add_edges([(4,5), (4,1), (5,1)])     # Ajout d'arêtes qui laissent le graphe bien formé 
        self.assertTrue(o5.is_well_formed())

        o5.get_node_by_id(5).add_children_id(1) # Action plus ou moins 'illégale', on devrait moralement faire ici un add edge.
        self.assertFalse(o5.is_well_formed())   # On vérifie ici que si la multiplicité ne correspond pas entre deux noeuds, le graph n'est pas bien formé.
        o5.get_node_by_id(5).remove_child_once(1)
        o5.get_node_by_id(5).add_parent_id(4)
        self.assertFalse(o5.is_well_formed())   # De même que ci dessus, on vérifie ici l'inverse, c'est a dire si la multiplicité d'un enfant ne correspond pas a celui de son parent.
        

    def test_shift_indice(self):
        o1 = open_digraph().empty()
        o2 = o1.copy()
        o1.shift_indices(2)
        self.assertEqual(o1, o2) # Edge case : Shift l'indice sur un graphe vide ne devrait pas avoir d'effet.

        for _ in range(10):
            o1.add_node()
        for i in range(5):
            o1.add_edge(i+1, i+2) # On va vérifier que le shift indice fonctionne aussi en testant avec des edges
        
        o1.add_input_node(2)
        o1.add_input_node(3)

        o2 = o1.copy()
        
        self.assertTrue(o1.is_well_formed()) # Ce assert ne vérifie pas si shiftIndice fonctionne mais vérifie que le test est cohérent
        print(o2)
        o2.shift_indices(2)
        self.assertTrue(o1.is_well_formed()) # On vérifie ici que le shift indice a gardé la cohérence de o1
        print(o2)
        o2.shift_indices(-2)
        print(o2)
        self.assertTrue(o1.is_well_formed()) # On va vérifier que les deux shift se sont équilibrés, et que l'on n'a pas perdu de données entre temps.
        self.assertEqual(o1, o2)

    def test_djikstra(self):

        o1 = open_digraph.empty()
        for _ in range(5):
            o1.add_node()

        o1.add_edge(1, 2)
        o1.add_edge(2, 4)
        o1.add_edge(4, 3)
        o1.add_edge(3, 4)
        o1.add_edge(2, 1)
        o1.add_edge(1, 5)
        # o1.display() # On a utilisé ici un display pour réaliser le test
        with self.assertRaises(ValueError):
            o1.dijkstra(6)                                                                  # 6 n'étant pas dans le graphe, on attend évidamment une erreur.
       
        self.assertEqual(o1.dijkstra(1), ({1:0, 2:1, 5:1, 4:2, 3:3}, {2:1, 5:1, 4:2, 3:4})) # Le test a été réalisé a la main avec un display.
        
        self.assertEqual(o1.dijkstra(1, direction=-1), ({1:0, 2:1}, {2:1}))
        self.assertEqual(o1.dijkstra(3, direction=1), ({3:0, 4:1}, {4:3}))                  # Test également réalisé a la main pour vérifier que direction=1 fonctionne.        
        self.assertEqual(o1.dijkstra(3, direction=-1), ({3:0, 4:1, 2:2, 1:3}, {4:3, 2:4, 1:2}))                  # Test également réalisé a la main pour vérifier que direction=1 fonctionne.        
        self.assertEqual(o1.dijkstra(1, tgt=2), ({1:0, 2:1}, {2:1}))    # Test de l'argument tgt pour vérifier que l'algorithme s'arrête bien quand il est trouvé

        # En se basant sur les test ci dessus, on peut facilement élaborer des test pour shortest path
        self.assertEqual(o1.shortest_path(1, 1), []) # Edge case évident : La node d'arrivée est égale a la node de départ
        self.assertEqual(o1.shortest_path(1, 3), [2,4])

        # Quelques tests de ancetre commun
        self.assertEqual(o1.ancetre_commun(1, 1), {1:(0,0), 2:(1,1)})
        self.assertEqual(o1.ancetre_commun(2, 5), {1:(1,1), 2:(0,2)})


    def test_tri_topologique(self):
        o = open_digraph.random(5, 6, form='undirected')
        with self.assertRaises(Exception): # On vérifie ici que un graph acyclique lève bien une erreur
            o.tri_topologique()
        o2 = open_digraph.empty()
        for i in range(5):
            o2.add_node(i)
        for i in range(4):
            o2.add_edge(i+1, i+2)
        self.assertEqual(o2.tri_topologique(), [[1], [2], [3], [4], [5]]) # Un petit test simple de tri_topologique

        # Le même test que dans le sujet sujet:
        o3 = open_digraph.empty()
        for i in range(10):
            o3.add_node()
        o3.add_edge(1, 4)
        o3.add_edge(2, 5)
        o3.add_edge(2, 6)
        o3.add_edge(2, 9)
        o3.add_edge(3, 5)
        o3.add_edge(4, 6)
        o3.add_edge(4, 7)
        o3.add_edge(4, 8)
        o3.add_edge(5, 7)
        o3.add_edge(6, 8)
        o3.add_edge(7, 9)
        o3.add_edge(7, 10)

        self.assertEqual(o3.tri_topologique(), [[1,2,3], [4,5], [6,7], [8,9,10]])

        self.assertEqual(o3.longest_path(1, 1), ([], 0))
        with self.assertRaises(Exception): # On vérifie que l'exception quand l'entrée n'est pas dans le graphe fonctionne
            o3.longest_path(-1, 1)
        with self.assertRaises(Exception): # On vérifie que l'exception quand l'arrivée n'est pas dans le graphe fonctionne
            o3.longest_path(11, 1)

        self.assertEqual(o3.longest_path(1, 8), ([4,6], 3))
    def test_open_digraph_from_string(self):
        g = bool_circ.from_string('((x0)&((x1)&(x2)))|((x1)&(~(x2)))')
        self.assertTrue(g.is_well_formed())
        #g.display()

        g2 = bool_circ.from_string("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        self.assertTrue(g2.is_well_formed())
        #g2.display()

        g3 = bool_circ.from_string("((x0)&(x1)&(x2))|((x1)&(~(x2)))") 
        self.assertTrue(g3.is_well_formed())
        #g3.display()

    def test_matrix_digraph(self):
        n = 5
        bound = 25
        m = random_matrix(n, bound)
        o2 = open_digraph.graph_from_adjacency_matrix(m)

        self.assertEqual(len(o2.get_nodes()), 5)
        for i in range(len(m)):                     # On va vérifier pour chacune des valeurs de la matrice que un edge correspondant est bien présent dans le graphe.
            for j in range(len(m)):
                if m[i][j] > 0:
                    self.assertEqual(m[i][j], o2.get_node_by_id(i+1).children[j+1])
        
        o2 = open_digraph.random(n, bound, form="free") # On vérifie ici simplement que la forme ne génère pas d'erreur
        
        o2 = open_digraph.random(n, bound, form="DAG")
        self.assertFalse(o2.is_cyclic())
        
        o2 = open_digraph.random(n, bound, form="oriented")
        # On vérifie ici que o2 n'a aucune arrête qui va dans les deux sens 
        # i.e que si une node d'id a a un child d'id b, alors b n'a pas de child d'id a.
        for noeud in o2.get_nodes():
            for c in noeud.get_children_ids():
                self.assertFalse(c in o2.get_node_by_id(c).get_children_ids())
       
        o2 = open_digraph.random(n, bound, form="loop-free")
        # On Vérifie ici que o2 n'a aucun noeud avec une arrête qui va vers lui même
        for noeud in o2.get_nodes():
            self.assertFalse(noeud.get_id() in noeud.get_children_ids())

        o2 = open_digraph.random(n, bound, form="undirected")
        # On vérifier ici que o2 est symmétrique (Que si un noeud a une arrête de multplicité x vers b, alors b a également une arrête de multiplicité x vers a)
        for noeud in o2.get_nodes():
            for child in noeud.get_children_ids():
                self.assertEqual(noeud.get_children_mult(child), o2.get_node_by_id(child).get_parent_mult(noeud.get_id()))
        

        o2 = open_digraph.random(n, bound, form="loop-free undirected")
        # TODO : Vérifier ici que o2 est symmétrique ET n'a aucun node qui pointe vers lui même

        m = open_digraph.random(5, 5, 3, 3)
        m.save_as_dot_file()
        m2 = open_digraph.from_dot_file("Out.dot")

        self.assertEqual(m, m2)

if __name__ == '__main__':  # the following code is called only when
    unittest.main()         # precisely this file is run
