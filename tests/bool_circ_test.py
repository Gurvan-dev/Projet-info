import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *


class InitTest(unittest.TestCase):
    def test_from_string(self):
        g = bool_circ.from_string('((x0)&((x1)&(x2)))|((x1)&(~(x2)))')
        self.assertTrue(g.is_well_formed())
        #g.display() # Utilisé pour vérifier a la main que le résultat était également cohérent

        g2 = bool_circ.from_string("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        self.assertTrue(g2.is_well_formed())
        self.assertTrue(len(g2.outputs) == 2)
        self.assertTrue(len(g2.inputs) == 3)
        #g2.display() # Utilisé pour vérifier a la main que le résultat était également cohérent

        g3 = bool_circ.from_string("((x0)&(x1)&(x2))|((x1)&(~(x2)))") 
        self.assertTrue(g3.is_well_formed())
        self.assertTrue(len(g3.outputs) == 1)
        self.assertTrue(len(g3.inputs) == 3)
        #g3.display() # Utilisé pour vérifier a la main que le résultat était également cohérent

    def test_from_table(self):
        # Les tests ci-dessous ont été ré-écrit pour être plus précis avec des outils développés dans les TDs suivant le TD
        # dans lequelle la fonction 'from_table' a été implémentée.
        table = '0111' # Cette table doit renvoyer 0 si les deux inputs sont 0 et 1 dans tout les autres cas.
        table_graph = bool_circ.from_table(table)
        test = [(0,'0'),(1,'1'),(2,'1'),(3,'1')] # On fait un tableau avec des tests : En premier l'input et en second le résultat attendu
        for (num, expected_output) in test:
            numbool = bool_circ.registre(num, 2) # On convertit le nombre en binaire ici pour l'utiliser en input
            t1 = bool_circ(table_graph.copy())
            t1.icompose(numbool)
            t1.evaluate()
            self.assertTrue(t1.get_output_str() == expected_output)
    
    def test_code_gray(self):
        with self.assertRaises(ValueError):
            bool_circ.code_gray(-1)
        self.assertEqual(bool_circ.code_gray(3), ['000', '001', '011', '010', '110', '111', '101', '100']) # Reprise de l'exemple donné dans l'énnoncé

    def test_k_map(self):
        self.assertEqual(bool_circ.K_map('1110001000111111'), [['1', '0', '1', '0'], ['1', '0', '1', '0'], ['0', '0','1','1'], ['1','1','1','1']]) # Reprise de l'exemple donnée dans l'énnoncé

    def test_random_bool(self):
        r1 = bool_circ.random_bool(10, inputs=5, outputs=3)
        self.assertTrue(len(r1.inputs) == 5)
        self.assertTrue(len(r1.outputs) == 3)
        self.assertTrue(r1.is_well_formed())
    
    def test_adder(self):

        # On va ici effectuer un test un peu couteux mais qui ne peut pas être plus précis :
        # On va simplement tester toutes les additions possible avec le adder, et vérifier qu'il rend bien le bon résultat
        # Note : On utilise déjà une fonction qui devrait en théorie être utilisée plus tard, à savoir registre.

        #  Le test étant plutôt conséquent en terme de performance, ce paramètre a été abaissé a 1 pour qu'au premier lancement les tests soit rapide.
        # Il a néanmoins été testé avec une plus grande valeur. 

        taille_adder = 1 
        taille_reelle = 2**taille_adder

        halfadd = bool_circ.half_adder(taille_adder)
        
        for a in range(2**taille_reelle):
            for b in range(2**taille_reelle):
                addcop = bool_circ(halfadd.copy())
                abc = bool_circ.registre(a, taille_reelle)
                bbc = bool_circ.registre(b, taille_reelle)
                abc.iparallel(bbc)
                addcop.icompose(abc)
                addcop.evaluate()
                res = addcop.get_output_str()
                self.assertTrue(int(res,2) == (a+b))

    def test_registre(self):

        res = bool_circ.registre(0,1)
        res.evaluate()
        res_str = res.get_output_str()
        self.assertTrue('0' == res_str)

        res = bool_circ.registre(1,1)
        res.evaluate()
        res_str = res.get_output_str()
        self.assertTrue('1' == res_str)

        res = bool_circ.registre(2,2)
        res.evaluate()
        res_str = res.get_output_str()
        self.assertTrue('10' == res_str)

    def test_evaluate(self):
        ...

    def test_simplify(self):
        # On va éfféctuer un test plutôt simple : 
        # On va générer un circuit aléatoire, et en faire deux copie.
        # On va ensuite choisir un input au hasard pour ce circuit
        # Sur la première copie, on va simplement évaluer le circuit
        # Sur la deuxième copie, on va d'abord simplifier le circuit, puis l'évaluer
        # On peut ensuite comparer les deux résultats et conclure
        nombre_de_test = 250
        rand_nombre = 3

        for _ in range(nombre_de_test):
            rand = bool_circ.random_bool(10, inputs=4, outputs=4)
            rand_nombre_bool = bool_circ.registre(rand_nombre, 4)
            rand_deux = rand_nombre_bool.copy()

            rand_premier = bool_circ(rand.copy())
            rand_premier.icompose(rand_nombre_bool)
            rand_premier.evaluate()
            premier_res = rand_premier.get_output_str()

            rand.simplify()
            rand.icompose(rand_deux)
            rand.evaluate()
            second_res = rand.get_output_str()

            self.assertTrue(premier_res == second_res)

if __name__ == '__main__':  # the following code is called only when
    unittest.main()         # precisely this file is run
