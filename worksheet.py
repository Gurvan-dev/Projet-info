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


#s = '1100000001010111'
#a = bool_circ.from_table(s)


#print(bool_circ.code_gray(1))
#print(bool_circ.code_gray(2))
#print(bool_circ.code_gray(3))

#print(bool_circ.K_map(s))

#bool_circ.random_bool(10, inputs=11, outputs=24).display()
#add0 = bool_circ.adder(1)
#print(add0.inputs)
#add0.display()
#bool_circ.adder(1).display()

#a = 32
#b = 57
#taille = 8
#abc =  bool_circ.registre(a, taille)
#bbc = bool_circ.registre(b, taille)
#abc.iparallel(bbc)
#add = bool_circ.half_adder(3)
#add.display()
#add.icompose(abc)

#add.evaluate()
#c = bool_circ.registre((a+b),taille)
#add.display()
#c.display()
#print(c)
#print(add)

#test = bool_circ.from_string("(x1)^(x3)^(x4)", "(x1)^(x3)^(x4)","(x1)","(x2)^(x3)^(x4)", "(x2)", "(x3)", "(x4)")
#test.display()

#enc = bool_circ.encoder()


#helpme = bool_circ.registre(5, 4)
#dec = bool_circ.decoder()
#enc = bool_circ.encoder()
#dec.icompose(enc)
#dec.icompose(helpme)
#dec.display()
#dec.evaluate()
#dec.display()
#print(dec)

#a = 5
#b = 5
#encodage = 2
#encodage_reel = 2**encodage
#abc = bool_circ.registre(a, encodage_reel)
#bbc = bool_circ.registre(b, encodage_reel)
#ayder = bool_circ.half_adder(encodage)
#abc.iparallel(bbc)

#ayder.display()
#ayder.icompose(abc)

#ayder.display()
#print(ayder)
#ayder.evaluate()
#print(ayder)
#print(f"{bin(a)} {bin(b)}")
#ayder.display()
#print(bin((a+b)))
#print(ayder.get_output_str())
#print(int(ayder.get_output_str(), 2))

#rand = bool_circ(open_digraph.from_dot_file('erreur.dot'))
#rand.display()
#rand.simplify()
#rand.display()

test_range = 100
tot = 0
for _ in range(test_range):
    rand = bool_circ.random_bool(20,5,5)
    rand.save_as_dot_file('erreur.dot')
    #rand.display()
    pre = len(rand.nodes)
    rand.simplify()
    post = len(rand.nodes)
    tot = tot + (pre - post)

print(tot)
print(tot/test_range)

#helpme.display()
#dec.icompose(helpme)
#dec.evaluate()
#dec.display()