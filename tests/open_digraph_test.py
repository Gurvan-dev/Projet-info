import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.open_digraph import *


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
        o2.nodes = [node(0, 'i', {}, {1: 1})]

        self.assertNotEqual(o.inputs, o2.inputs)
        self.assertNotEqual(o.outputs, o2.outputs)
        self.assertNotEqual(o.nodes, o2.nodes)
        self.assertEqual([], o.get_nodes())
        o2.add_node()
        print(o.get_nodes())
        self.assertEqual(o2.get_nodes(), [node(0, 'i', {}, {1: 1})])       #, node(1, '', {}, {}) ] )


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
