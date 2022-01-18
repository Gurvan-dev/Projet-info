from modules.open_digraph import *

#print("hello world")
n0 = node(42, 'i', {}, {1:1}) 
o = open_digraph( [0, 1, 2, 7], [0], [n0])

print(f"\n n0 : \n {n0} \n\n o = \n{o}\n")