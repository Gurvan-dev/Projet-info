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
        o2.nodes = {node.id : node for node in [node(1, 'i', {}, {1: 1})]}

        self.assertNotEqual(o.inputs, o2.inputs)
        self.assertNotEqual(o.outputs, o2.outputs)
        self.assertNotEqual(o.nodes, o2.nodes)
        self.assertEqual([], o.get_nodes())
        o2.add_node()
        #print(f"o2 nodes = {o2.nodes}")
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

        self.assertEqual(n1.get_children_id(), {2:4, 3:8})
        self.assertEqual(n2.get_children_id(), {1: 2, 2:2, 3:4})

        n1.remove_parent_id(2)
        n2.remove_parent_id(3)

        self.assertEqual(n1.get_parents_ids(), {1:2, 3:1})
        self.assertEqual(n2.get_parents_ids(), {1:5})

        n1.remove_child_id(3)
        n2.remove_child_id(1)

        self.assertEqual(n1.get_children_id(), {2:4})
        self.assertEqual(n2.get_children_id(), {2:2, 3:4})

        # Exercice 2

        n1 = node(1, 'i', {1:2, 2:3, 3:1}, {1: 1, 2:4, 3:8})
        n2 = node(2, 'j', {1:5, 2:1, 3:2}, {1: 2, 2:2, 3:5})

        o3 = o.copy()
        o3.outputs = [0, 1, 2, 7]
        o3.nodes = {node.id : node for node in [n1, n2]}

        o3.remove_edge()

        #print(f"o3 nodes = {o3.nodes} \n")
        #o3.get_node_by_id(1).remove_parent_once(2)
        #o3.get_node_by_id(1).remove_child_once(2)

        #print(f"o3 nodes = {o3.nodes} \n")

        #print(type(o3))
        #print(f"o3 nodes = {o3.nodes} \n")
        #print(f"o3 nodes = {o3.nodes} \n")
        #print(f"o3 nodes = {o3.nodes} \n")



if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
