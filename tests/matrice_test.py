import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.matrice import *


class InitTest(unittest.TestCase):
    def test_matrice(self):

        self.assertEqual(len(random_int_list(5, 20)), 5)

        m = random_matrix(6, 75)
        self.assertEqual(len(m), 6)
        for i in m:
            self.assertEqual(len(m), 6)
        
        m = random_matrix(9, 70, null_diag=True)
        for i in range(len(m)):
            self.assertEqual(m[i][i], 0)

        m = random_matrix(9, 70,null_diag=True, symmetric=True)
        for i in range(len(m)):
            for j in range(len(m)):
                self.assertEqual(m[i][j], m[j][i])

        #oriented

        m = random_matrix(9, 25, oriented = True)
        #print("[  ")
        #for i in range(len(m)):
        #    print("[  ")
        #    for j in range(len(m)):
        #        print(f"  {m[i][j]}  ")
        #    print("]")
            #print("\n")
        #print("]")
        print(m)

        for i in range(len(m)):
            for j in range(len(m)):
                if m[i][j] > 0 and i != j:
                    self.assertEqual(m[j][i], 0)

        




         
         
        # #triangular






if __name__ == '__main__':  # the following code is called only when
    unittest.main()         # precisely this file is run
