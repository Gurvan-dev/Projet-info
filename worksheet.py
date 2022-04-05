from modules.open_digraph import *
from modules.bool_circ import *
import inspect

#print(dir(node))
#print(dir(open_digraph.empty))

#print("\n")

#print(inspect.getdoc(node.__init__))
#print("\n")
#print(inspect.getsource(node.__init__))
#print("\n")
#print(inspect.getfile(node.__init__))
#print("\n")

#m = open_digraph.random(5, 5, 3, 3)
#m.get_node_by_id(1).set_label('cool') # label cool
# m.display()
#m2 = m.from_dot_file('tmp.dot')

#m2.iparallel(m)
#m2.display()
#print(m2.connected_components())


s = '1100000001010111'
a = bool_circ.from_table(s)



print(bool_circ.code_gray(1))
print(bool_circ.code_gray(2))
print(bool_circ.code_gray(3))

print(bool_circ.K_map(s))