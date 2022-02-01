import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.matrice import *


class InitTest(unittest.TestCase):
    def test_matrice(self):
        self.assertTrue(True)
        





if __name__ == '__main__':  # the following code is called only when
    unittest.main()         # precisely this file is run
