from modules.open_digraph import *
from modules.bool_circ import *
import inspect

# Ci dessous un test pour connaître le nombre de node retiré en moyenne par une simplification

test_range = 250
taille_node = 10
tot = 0
for _ in range(test_range):
    rand = bool_circ.random_bool(taille_node,5,5)
    #rand.save_as_dot_file('erreur.dot')
    #rand.display()
    pre = len(rand.nodes)
    rand.simplify()
    post = len(rand.nodes)
    tot = tot + (pre - post)

print(tot)
print(tot/test_range)

# Quelques résultats obtenus avec une test_range = 250: 
# taille_node : (tot/test_range)
# 50 : 4.556
# 20 : 4.08
# 10 : 3.236

# On note que le nombre de node retiré par la simplification n'est pas du tout proportionel au nombre de noeud dans le circuit.
# On peut expliquer ça de différentes façons:
# La simplification peut également ajouter des noeuds, qui peuvent compense l'ajout d'autres noeuds.
# La complexité du circuit augmente quand la taille du circuit augmente, et cette complexité peut ne pas être simplifiable

# Ci dessous on va vérifier que l'encoder-décoder permet bien de conserver les données.

enc = bool_circ.encoder()
i_test = 3
num = bool_circ.registre(i_test, 4)
enc.icompose(num)
enc.evaluate()
enc.display()
num.evaluate()

# On va créer un bruit en changeant tout les bits et vérifier que le décodeur rend bien le même résultat
for i in range(len(enc.outputs)):
    enc_copy = bool_circ(enc.copy())
    out_node = enc_copy.get_node_by_id(enc_copy.outputs[i])
    dec = bool_circ.decoder()
    label = '0'
    if out_node.get_label() == '0':
        label = '1'
    out_node.set_label(label)

    dec.icompose(enc_copy)
    dec.evaluate()
    print(f"{num.get_output_str()} {dec.get_output_str()}")

# Après un lancement, on remarque bien que le bruit n'affecte pas le résultat final.
# On va ensuite vérifier qu'en changeant deux noeuds, la donnée initiale est bien perdue:

enc_copy = bool_circ(enc.copy())
enc_copy.display()
out_node = enc_copy.get_node_by_id(enc_copy.outputs[0])
label = '0'
if out_node.get_label() == '0':
    label = '1'
out_node.set_label(label)

out_node = enc_copy.get_node_by_id(enc_copy.outputs[1])

label = '0'
if out_node.get_label() == '0':
    label = '1'
out_node.set_label(label)

enc_copy.display()

dec = bool_circ.decoder()
dec.icompose(enc_copy)
dec.evaluate()
print(f"{num.get_output_str()} {dec.get_output_str()}")

# On voit bien que ce n'est plus la même chose et que la donnée initiale est perdue.

# On va vérifier aussi que le décodeur et l'encoder composé donnent bien l'identité

id = bool_circ.decoder()
id.icompose(bool_circ.encoder())
id.simplify()
id.display()