from modules.open_digraph import *
import inspect

print(dir(node))
print(dir(open_digraph.empty))

print("\n")

print(inspect.getdoc(node.__init__))
print("\n")
print(inspect.getsource(node.__init__))
print("\n")
print(inspect.getfile(node.__init__))
print("\n")

m = open_digraph.random(10, 5)
m.get_node_by_id(1).label = 'AAAAAAAAA'
m.save_as_dot_file(verbose=True)
open_digraph.from_dot_file("Out.dot")