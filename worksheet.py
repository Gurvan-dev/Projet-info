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

