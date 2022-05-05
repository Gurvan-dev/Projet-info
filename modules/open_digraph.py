from modules.matrice import *
from modules.node import *
from random import randint
from math import log
import os
import re
import sys

class open_digraph:
	def __init__(self, inputs=[], outputs=[], nodes=[]):
		'''
		inputs: int list; the ids of the input nodes
		outputs: int list; the ids of the output nodes
		nodes: node iter;
		'''
		self.inputs = inputs.copy()     # On réalise ici des copie afin d'être sûr d'éviter toute confusion pendant l'utilisation de la classe.
		self.outputs = outputs.copy()   # Une liste donnée en paramètre peut ainsi être ré-utilisée plus tard sans aucune incidence sur ce graphe.
		self.nodes = {node.id: node.copy() for node in nodes} # self.nodes: <int,node> dict
		if self.nodes == {}:    # On initialise ici un compteur qui va permettre d'avoir un ID unique pour chaque node,
			self.c = 0          # sans risque de ré-attribution d'un même id a plusieurs node,
		else:                   # et ce même après suppression ou ajout de plusieurs node. 
			self.c = max([node.id for node in nodes])

	def __str__(self) -> str:
		return f"Input : {self.inputs}   Output : {self.outputs}   Nodes : {[node for node in self.nodes]}"

	def __repr__(self) -> str:
		return f" Digraph({self})"

	def copy(self):
		return open_digraph(self.inputs, self.outputs, self.nodes.values()) # On peut juste renvoyer un nouveau digraph avec comme paramètre les valeurs des variables actuels, car un copy est des le constructeur.

	def __eq__(self, other) -> bool:
		return self.inputs == other.inputs and other.outputs == other.outputs and self.nodes == other.nodes

	def sort(self):
		c = {}
		for k in sorted(self.nodes.keys()):
			c[k] = self.nodes[k]
		self.nodes=c

	@classmethod
	def empty(cls):
		'''
		Return an empty open digraph.
		'''
		return open_digraph([], [], [])

	def get_input_ids(self):
		return self.inputs

	def get_output_ids(self):
		return self.outputs
	
	def get_id_node_map(self):
		return self.nodes

	def get_nodes(self):
		return list(self.nodes.values())

	def get_nodes_ids(self):
		return list(self.nodes.keys())
	
	def get_node_by_id(self, i : int):
		''' 
		i	: int, un id du graphe
		'''
		return self.nodes[i]

	def get_nodes_by_ids(self, t):
		''' 
		t		: int list, une liste d'id du graphe
		return	: node list, la liste de node avec les ids correspondant a ceux présents dans t
		'''
		res = []
		for i in t:
			res.append(self.nodes[i])
		return res

	def set_input_ids(self, ids):
		self.inputs = ids
	
	def set_output_ids(self, ids):
		self.outputs = ids

	def add_input_id(self, id : int):
		if id not in self.inputs:
			self.inputs.append(id)

	def add_outputs_id(self, id : int):
		if id not in self.outputs:
			self.outputs.append(id)

	def new_id(self):
		self.c = self.c + 1
		return self.c

	def add_edge(self, src : int, trg : int, mult = 1):
		self.get_node_by_id(src).add_children_id(trg, mult)
		self.get_node_by_id(trg).add_parent_id(src, mult)
	
	def add_edges(self, edgeList):
		for (src, trg) in edgeList:
			self.add_edge(src,trg)
	
	def add_node(self, label='', parents={}, children={}, id = 0) -> int:
		'''
		label		: str, Le nom de la node
		parents		: dic : int -> int, Les parents de la node avec leurs multiplicité
		childrens 	: dic : int -> int, Les childrens de la node avec leurs multiplicité
		id			: [Optional] int positif, l'id de la node a ajouter. Aucune vérification ne sera faite si l'id est déjà présent dans le graphe
		return		: int, l'id de la node ajouté. égal a id si précisé.
		Ici les paramètres possèdent des noms plutôt explicite quant a leurs fonctions.
		Les parents ne seront pas directement ajouté a la node,
		mais seront plutôt utilisé comme argument pour faire des add_edge.
		De cette façon, on s'assure que le graphe soit bien formé qu'importe l'utilisation de add_node
		(Le seul moyen pour que le graphe soit mal formé étant ainsi une erreur)
		'''
		if parents is None:
			parents={}
		if children is None:
			children={}
		
		if id <= 0:
			id = self.new_id()
		
		self.nodes[id] = node(id, label, {}, {})
		for p in parents:
			self.add_edge(p, id, parents[p])
		for c in children:
			self.add_edge(id, c, children[c])
		return id

	def add_input_node(self, id : int, id_added=0) -> int:
		'''
		id			: int, L'id sur laquelle greffer une nouvelle node qui sera une input node liée par une arrête a cette première.
		id_added	: int, L'id de l'input qu'on va ajouter. Si aucune valeur n'est spécifiée ou si la valeur est >= 0, on va attribuer une valeur aléatoire.
		Throw une exception si la node sur laquelle on doit se greffer est elle même une input node, afin que le graphe reste bien formé.
		'''
		# Pour garder un graphe bien formé en toute circonstance, on vérifie que on n'ajoute pas un input devant un autre input.

		if id in self.inputs:
			raise Exception('Tentative d\'ajouter un input sur un input.')
		if id_added <= 0:
			id_added = self.add_node()
		else:
			self.add_node(id=id_added)
		self.add_edge(id_added, id)
		self.add_input_id(id_added)
		return id_added

	def add_output_node(self, id : int, id_added=0) -> int:
		'''
		id			: int, L'id sur laquelle greffer une nouvelle node qui sera une output node liée par une arrête a cette première.
		id_added	: int, L'id de l'input qu'on va ajouter. Si aucune valeur n'est spécifiée ou si la valeur est >= 0, on va attribuer une valeur aléatoire.
		Throw une exception si la node sur laquelle on doit se greffer est elle même une output node, afin que le graphe reste bien formé.
		'''
		# Pour garder un graphe bien formé en toute circonstance, on vérifie que on n'ajoute pas un output derrière un autre output.
		if id in self.outputs:
			raise Exception('Tentative d\'ajouter un output derrière un output.')
		if id_added <= 0:
			id_added = self.add_node()
		else:
			self.add_node(id=id_added)
		self.add_edge(id, id_added)
		self.add_outputs_id(id_added)
		return id_added

	def remove_edge(self, src : int, trg : int):
		'''
		src : int, la noeud de départ de l'arrête a retirer
		trg : int, le noeud d'arrivée de l'arrêtre a retirer
		Enlève une arrête de src vers trg.
		'''
		self.get_node_by_id(trg).remove_parent_once(src)
		self.get_node_by_id(src).remove_child_once(trg)

	def remove_parallel_edge(self, src : int, trg : int):
		''' 
		src : int, la noeud de départ de l'arrête a retirer
		trg : int, le noeud d'arrivée de l'arrêtre a retirer
		Enlève toutes les arrêtes de src vers trg.
		'''
		self.get_node_by_id(trg).remove_parent_id(src)
		self.get_node_by_id(src).remove_child_id(trg)

	def remove_edges(self, listEdge):
		''' 
		listEdge	: int list, une liste d'edge (Couple (int,int)) a retirer.
		'''
		for (src, trg) in listEdge:
			self.remove_edge(src, trg)

	def remove_parallel_edges(self, listEdge):
		''' 
		listEdge	: int list, une liste d'edge (Couple (int,int)) a retirer. Retire toute la multiplicité de ces dernières
		'''
		for (src, trg) in listEdge:
			self.remove_parallel_edge(src, trg)

	def remove_node_by_id(self, id):
		''' 
		id	: int, L'id d'une node du graph
		Supprime la node du graphe, ainsi que les arrête qui y passent
		'''
		n = self.nodes.pop(id)
		n_id = n.get_id()
		if n_id in self.inputs:
			self.inputs.remove(n_id)
		if n_id in self.outputs:
			self.outputs.remove(n_id)
		for p in n.get_parents_ids():
			if p in self.nodes:
				self.get_node_by_id(p).remove_child_id(n_id)
		for c in n.get_children_ids():
			if c in self.nodes:
				self.get_node_by_id(c).remove_parent_id(n_id)
		
	def remove_nodes_by_id(self, ids):
		'''
		ids : int list, une liste d'id de  node a retirer.
		'''
		for id in ids:
			self.remove_node_by_id(id)

	def remove_all_parents(self, id : int):
		''' 
		id : int, un id du graphe
		retirer tout ses parents a id
		'''
		id_node = self.get_node_by_id(id)
		while len(id_node.get_parents_ids()) > 0:
			par = list(id_node.get_parents_ids())[0]
			self.remove_parallel_edge(par, id)

	def remove_all_childrens(self, id : int):
		''' 
		id : int, un id du graphe
		retirer tout ses enfants a id
		'''
		id_node = self.get_node_by_id(id)
		while len(id_node.get_children_ids()) > 0:
			chi = list(id_node.get_children_ids())[0]
			self.remove_parallel_edge(id, chi)

	def is_well_formed(self):
		''' 
		Renvoie vrai si le graph est bien formé, i.e. :
		- Que tout les inputs sont bien présents dans le graphe (resp output)
		- Que les inputs n'ont pas de parents (resp output, children)
		- Que la multiplicité est toujours égale dans une relation parents enfants 
		- Que les clés des node dans le graph sont bien les id des nodes
		'''
		for n in self.inputs:
			if not (n in self.nodes): # Vérifier que tout les éléments d'input sont dans le graphe.
				return False
			if len(self.get_node_by_id(n).get_children_ids()) != 1: # Vérifier que les inputs n'ont qu'un enfant
				return False 
			if len(self.get_node_by_id(n).get_parents_ids()) > 0: # Vérifier que les inputs n'ont pas de parents
				return False 
			if self.get_node_by_id(n).outdegree() != 1:
				return False
		for n in self.outputs:
			if not (n in self.nodes): 
				return False
			if len(self.get_node_by_id(n).get_parents_ids()) != 1: # Vérifier que les outputs n'ont qu'un parent
				return False 
			if len(self.get_node_by_id(n).get_children_ids()) > 0: # Vérifier que les outputs n'ont pas d'enfants
				return False
			if self.get_node_by_id(n).indegree() != 1:
				return False
		for key in self.nodes.keys():
			if(self.get_node_by_id(key).get_id() != key): # Vérifier que les cléfs de nodes correspondent a l'id.
				return False

		# Vérifier que la multiplicité est bien la même pour un parent et un enfant.
		for j in self.nodes.values():
			for i in j.get_children_ids().keys():
				if not i in self.nodes.keys():
					return False
				n = self.get_node_by_id(i)
				if not (j.get_id() in n.get_parents_ids()) or j.get_children_ids()[i] != n.get_parents_ids()[j.get_id()]:
					return False
			for i in j.get_parents_ids().keys():
				if not i in self.nodes.keys():
					return False
				n = self.get_node_by_id(i)
				if not (j.get_id() in n.get_children_ids()) or j.get_parents_ids()[i] != n.get_children_ids()[j.get_id()]:
					return False
		
		return True
	
	def min_id(self):
		'''
		return	: int, le plus petit indice d'id du graph
		'''
		return min(self.nodes.keys())
		
	def max_id(self):
		'''
		return	: int, le plus grand indice d'id du graph
		'''
		if len(self.nodes) > 0:
			return max(self.nodes.keys())
		else:
			return 0

	def shift_indices (self,shift : int):
		'''
		shift : int, Un entier quelconque. (n=0 n'aura aucun effet sur le graphe)
		'Shift les indice' de toutes les nodes du graph, i.e déplace tout les ids des nodes de 'n'.
		'''
		self.c = self.c + shift
		old_new = []
		key_inv = sorted(self.nodes.keys())
		if shift > 0: # Si on doit faire un shift positif, on va d'abord décaler les plus grands nombre puis les plus petits, afin de ne pas écraser de donnée.
			key_inv.reverse()
		for key in key_inv:
			self.nodes[key].shift_indice(shift)
			old_new.append((self.nodes[key], key+shift))
		for (o,n) in old_new:
			self.nodes[n] = o
			self.nodes.pop(o.get_id())
			o.set_id(n)

		new_input = []
		for i in self.inputs:
			new = i+shift
			new_input.append(new)
		self.inputs = new_input
		new_outputs = []
		for i in self.outputs:
			new = i+shift
			new_outputs.append(new)
		self.outputs = new_outputs
			
	def iparallel(self, g):
		'''
		Modifie le graph pour y ajouter g en parallèle, i.e. les deux parties seront dans le même open digraph mais ne seront pas connexe.
		'''
		M = self.max_id()
		m = g.max_id()
		id_max = max(m, M) # Pour empêcher un chevauchement des ID ou des IDs qui sont les même dans les deux graph, on effectue un shife indice
		self.shift_indices(id_max)
		for n in g.get_nodes():
			n = n.copy()
			n_id = n.get_id()
			self.nodes[n_id] = n.copy()
		for inp in g.inputs:
			self.add_input_id(inp)
		for out in g.outputs:
			self.add_outputs_id(out)

	@classmethod
	def parallel(cls, a,b_list):
		cls = a.copy()
		for b in b_list:
			cls.iparallel(b.copy())
		return cls

	def icompose(self, g):
		''' 
		Modifie self pour y ajouter g en composition, i.e. on va connecter tout les output de g aux inputs de self
		Throw une exception si g n'a pas autant d'output que self a d'inputs (Car on ne peut pas les composer dans cette configuration)
		'''
		if len(self.inputs) != len(g.outputs):
			raise ValueError(f"Erreur: Tentative de composition entre deux graphe qui n'ont pas la même taille (inp : {len(self.inputs)} oup : {len(g.outputs)})")
		self.iparallel(g) # On va simplement les ajouter en parallel, puis relier les inputs et outputs qui doivent être relié.
		for new_in in g.outputs:
			self.outputs.remove(new_in)
			rem = self.inputs.pop(0)
			self.add_edge(new_in, rem)

	@classmethod
	def compose(cls, a,b_list):
		cls = a.copy()
		for b in b_list:
			cls.icompose(b.copy())
		return cls

	def connected_components(self):
		''' 
		return	: (int, int list list) les différentes parties connecté du graphe
		'''
		compte = 0
		closed = []
		dic_connexe = {}
		open = list(self.nodes.keys()).copy()
		
		while len(open) > 0:
			start = open.pop(0)
			
			if start not in closed:
				start_node = self.get_node_by_id(start) 
				closed.append(start) # La liste des fermés contient toutes les node qu'on a déjà vérifié. (Pour éviter récursion infinie)
				connexe_open = list(start_node.children.keys()).copy() # Connexe_open est une liste de tout les éléments relié a start_node d'une façon ou d'une autre (En tant que parents ou enfant)
				for p in start_node.parents:
					connexe_open.append(p)
			
				while len(connexe_open) > 0:
					cur = connexe_open.pop(0)
					
					if cur not in closed:
						cur_node = self.get_node_by_id(cur)
						closed.append(cur)
						dic_connexe[cur] = compte
						for child in cur_node.children:
							if child not in closed and child not in connexe_open:
								connexe_open.append(child)
						
						for par in cur_node.parents:
							if par not in closed and par not in connexe_open:
								connexe_open.append(par)
								closed.append(par)
				compte = compte+1
		return (compte, dic_connexe)
	   

	@classmethod
	def graph_from_adjacency_matrix(cls, mat):
		'''
		mat 	: int list list
		return	: open_digraph, open_digraph formed with the input matrix (See sujets/TD3.pdf).
		'''
		o = open_digraph.empty()
		for i in range(len(mat)):
			o.add_node()
		for x in range(len(mat)):
			for y in range(len(mat)):
					for _ in range(mat[x][y]):
						o.add_edge(x+1, y+1)  # Nos ids commencent par 1 donc +1
		return o

	@classmethod
	def random(cls, n : int, bound : int, inputs=0, outputs=0, form = "free"):
		'''
		n       : int, Nombre de noeuds dans le graphe
		bound   : int,  Nombre maximal de multiplicité pour une arrête
		inputs  : int, Nombre d'input a générer dans le graphe
		outputs : int, Nombre d'outputs a générer dans le graphe
		form : str,
			free                    : La matrice générée n'aura pas de contraintes.
			DAG                     : La matrice générée sera acyclique dirigé
			oriented                : La matrice générée sera orienté
			loop-free               : Un noeud ne pourra pas pointer sur lui même (Donc la diagonale de la matrice générée sera nulle)
			undirected              : La matrice sera symmétrique.
			loop-free undirected    : Combinaison de loop free et undirected
		Throw une ValueError si form n'est pas un str de la liste ci dessus.
		'''

		if form=="free":
			mat = random_matrix(n, bound)
		elif form=="DAG":
			mat = random_matrix(n, bound, triangular=True, null_diag=True)
		elif form=="oriented":
			mat = random_matrix(n, bound, oriented=True)
		elif form=="loop-free":
			mat = random_matrix(n, bound, null_diag=True)
		elif form=="undirected":
			mat = random_matrix(n, bound, symmetric=True)
		elif form=="loop-free undirected":
			mat = random_matrix(n,bound, symmetric=True ,null_diag=True)
		else:
			raise ValueError("Forme de matrice non correcte.")
			
		o = open_digraph.graph_from_adjacency_matrix(mat)

		for _ in range (inputs):
			o.add_input_node(randint(1, n))   # Nos ID commencent a 1, d'ou le 1, n+1.

		for _ in range (outputs):
			o.add_output_node(randint(1, n)) # Nos ID commencent a 1, d'ou le 1, n+1.
		
		return o

	def get_dic(self):
		'''
		return	: dictionnaire int -> int, associant a chaque id de noeud un unique entier 0 ≤ i < n
		'''
		dic = {}
		count = 0
		for nod in self.nodes.values():
			dic[nod.id] = count
			count = count + 1
		return dic

	def adjacency_matrix(self):
		'''
		return : matrice, La matrice d'adjacence associé au graph
		'''

		mat = []
		for _ in range (len(self.nodes)):
			mat.append([] * len(self.nodes))
		dic = self.get_dic()
		for node in self.nodes.values():
			i = dic[node.get_id()]
			for (child_id, mult) in node.get_children_ids():
				mat[i][child_id] = mult
		return mat
	
	def save_as_dot_file(self, path = 'Out.dot', verbose=False):
		''' 
		path	: str
		verbose	: boolean
		Enregistre le graph en tant que fichier .dot. path est le chemin + nom ou sera enregistré le fichier. 
		path devrait préférablement finir par '.dot'
		Les inputs seront représentés par des boîtes, tandis que les outputs seront représentée par de jolies étoiles.
		'''

		with open(path, 'w') as f:
			f.writelines("digraph G {\n")
			for node in self.nodes.keys():
				lab = self.get_node_by_id(node).get_label()
				param = ''
				if node in self.inputs:
					param = "shape= box "
				elif node in self.outputs:
					param = "shape= star "
				if verbose:
					f.writelines(f"\tv{node} [label=\"{lab} id=({node})\" {param}]\n")
				elif lab != '':
					f.writelines(f"\tv{node} [label=\"{lab}\" {param}]\n")
				elif param != '':
					f.writelines(f"\tv{node} [{param}]\n")

			for node in self.nodes.keys():
				n = self.get_node_by_id(node)
				
				name = ''.join([f'v{c} ' * n.get_children_mult(c) for c in n.get_children_ids()])
				name = '{' + name + '}'
				f.writelines(f"\tv{node} -> {name};\n" )
			f.writelines(("}"))

	@classmethod
	def from_dot_file(cls, path : str):
		''' 
		path	: str, doit mener vers un fichier .dot
		return	: open_digraph, construit depuis le fichier .dot se trouvant a 'path'.
		'''
		cls = open_digraph.empty()
		with open(path, 'r') as f:
			s = f.readline() # On enlève la première ligne inutile ici
			inp = []
			oup = []
			while s != "":
				s = f.readline()
				lesPtitsNombres = list(map(int, re.findall('\d+', s))) # On trouve tout les entiers sur la ligne
				if len(lesPtitsNombres) == 0:
					continue
				par = lesPtitsNombres[0] # parent : Le premier chiffre de la ligne
				
				if len(lesPtitsNombres) > 1: # On a une ligne avec plus de deux nombres : C'est une connection entre plusieurs node
					for i in range(1,len(lesPtitsNombres)):
						chi = lesPtitsNombres[i] #children
						if par in inp: # On a vx -> { y } qqchose avec x qui est une input node. Donc on crée une input node d'id x et on la greffe sur y.
							cls.add_input_node(id=chi,id_added=par)
						if chi in oup:
							cls.add_output_node(id=par,id_added=chi)
						else:
							if par not in cls.nodes.keys():
								cls.add_node(id = par)
							if chi not in cls.nodes.keys():
								cls.add_node(id = chi)
							cls.add_edge(par, chi)
				
				elif 'star' in s: 	# 'star' est utilisé pour les inputs.
					oup.append(par)
				elif 'box' in s: 	# 'box' est utilisé pour définir un output.
					inp.append(par)
				if 'label' in s:
					b,c,lab = s.partition('label') 			# On partitionne ici pour avoir tout ce qui est après le label. On doit peut être pouvoir l'intégrér a l'expression regex qui suit mais mes connaissances regex sont trop limitées.
					lab = re.findall('.*"(.*?)".*', lab)[0] # On regarde tout ce qu'il y a après le label entre guillemets,
															# et on prend le premier mot.			
					if par not in cls.nodes.keys():
						cls.add_node(id=par, label=lab)
					else:
						cls.get_node_by_id(par).set_label(lab)
		return cls

	def display(self):
		'''
		affiche le graphe.
		Note : firefox doit être installé.
		'''
		self.save_as_dot_file('tmp.dot')
		with open('tmp.dot', 'r') as f:
			t = f.read()
			t = t.replace('\n', '%0A%09')
			t = t.replace('\t', '')
			t = t.replace(';', '%3B')
			
			os.system("firefox -url 'https://dreampuf.github.io/GraphvizOnline#" + t + "'")

	def is_cyclic(self) -> bool:
		'''
		return	: boolean, vrai si le graphe est cyclique, faux sinon
		'''
		if self.get_nodes() == []:
			return False
		
		for i in self.get_nodes():
			if len(i.children) == 0:
				o = self.copy()
				o.remove_node_by_id(i.get_id())
				return o.is_cyclic()

		self.display()
		return True

	
	def dijkstra(self, src : int, direction = None, tgt = None):
		'''
		src : int, L'id de la node de départ
		direction : int,
			1		: Relation de parents vers enfant uniquement
			-1 		: Relation d'enfant a parent uniquement
			None	: Qu'importe le sens de la relation
		tgt : Si on recherche un chemin en particulier, une fois trouver, arrête la recherche de chemin.
		return : (dic int->int, dic int -> int) La distance depuis le noeud source jusqu'a chaque autre noeud, ainsi que le 'chemins' pour aller jusqu'a cet autre noeud. 
		Throw une ValueError si la source n'est pas dans le graphe
		'''
		if src not in self.nodes.keys():
			raise ValueError("L'entrée n'est pas dans le graphe.")
		opened = [src]
		dist = {src:0}
		prev = {}
		while opened != []:
			
			current = min(opened, key=dist.get)
			opened.remove(current)
			if direction == -1:
				neighbours = self.get_node_by_id(current).parents.copy() # On fait une copy pour ne pas modifier les parents en même temps que l'on fait dijkstra (Problème révélé par des tests)
			elif direction == 1:
				neighbours = self.get_node_by_id(current).children.copy()
			else:
				neighbours = self.get_node_by_id(current).parents.copy()
				for a in self.get_node_by_id(current).children.keys():
					neighbours[a] = self.get_node_by_id(current).children[a]
			for neigh in neighbours:
				if neigh not in dist:
					opened.append(neigh)
				if neigh not in dist or dist[neigh] > (dist[current] + 1):
					dist[neigh] = dist[current] + 1
					prev[neigh] = current
					if  tgt == neigh:
						return (dist, prev)	
		return (dist, prev)

	def shortest_path(self, src : int, tgt : int, direction = None):
		'''
		Doc
		src 	: L'id du node de départ
		tgt 	: L'id de la node d'arrivée
		return	: int list, le plus court chemin de src vers tgt.
		Throw une exception si la chemin n'existe pas, ou encore que src ou tgt n'est pas dans le graph. 
		'''
		# L'exception levée quand src n'est pas dans le graphe est en réalité levée par dijkstra et pas par shortest_path
		if src == tgt:
			return []
		dij = self.dijkstra(src, direction, tgt)[1] # On appelle dijkstra
		if tgt not in dij: 							# Si l'arrivée n'est pas dans le tableau, il n'y a aucun chemin qui va de a vers b avec la direction demandée.
			raise Exception("Path not found.")
		path = []
		cur = dij[tgt]
		while(cur != src): 		# On rebrousse chemin dans la liste des prev
			path.append(cur)
			cur = dij[cur]
		path = path[::-1]		# Comme on a rebroussé chemin, on doit inverser le chemin trouvé
		return path

	def ancetre_commun(self, a : int,b : int):
		'''
		a 		: int, Une id de node
		b 		: int, Une id de node
		return 	: dict (int, int), Un dictionnaire qui associe a chaque ancêtre commun des deux noeuds sa
		distance à chacun des deux noeuds
		'''
		dija = self.dijkstra(a, direction=-1)[0]
		dijb = self.dijkstra(b, direction=-1)[0]
		res = {}
		for id_n in dija:
			if id_n in dijb:
				res[id_n] = (dija[id_n], dijb[id_n])
		return res

	def tri_topologique(self):
		'''
		return	: int list list, le tri topologique du graphe. 
		(Regarder TP7 exercice 4)
		'''
		def tri_annexe(graph, depth, prev=[]): 				# On va ici utiliser une méthode récursive avec une sous fonction.
			prev.append([])									# On rajoute un étage de 'Pronfondeur'
			to_be_removed = []
			for i in graph.nodes.values():
				if len(i.parents) == 0: 					# On regarde si le graph d'id i est une co-feuilles i.e qu'il n'a pas de parents
					prev[depth].append(i.get_id()) 
			if prev[depth] == [] and len(graph.nodes) > 0: 	# Si il n'y a plus de co-feuilles et le graph est non vide, alors il est acyclique, donc on raise une erreur.
				raise Exception("Le graphe est acyclique.")
			for id in prev[depth]:							# On enlève toute les co-feuilles a l'instance de graphe actuelle
				graph.remove_node_by_id(id)
			if len(graph.nodes) == 0:						# Si le graph est vide ici, on a trouvé toutes les co-feuilles
				return prev
			return tri_annexe(graph, depth+1, prev)

		graph = self.copy() # On va faire une copie que l'on va utilisé pour le test, duquel on va retirer input et output (Ici on ignore les inputs et outputs.)
		for i in self.inputs:
			graph.remove_node_by_id(i)
		for o in self.outputs:
			graph.remove_node_by_id(o)
		
		return tri_annexe(graph, 0)

	def profondeur_node(self, id_node : int) -> int:
		'''
		id_node : int, l'id d'une node du graph
		return	: int, la profondeur de la node d'id 'id_graphe' ou -1 si id_node n'est pas dans le graphe.
		'''
		tt = self.tri_topologique()
		for d in range(len(tt)):
			if id_node in tt[d]:
				return d
		return -1
	
	def profondeur_graph(self) -> int:
		'''
		return	: int, la profondeur du graphe, i.e. la profondeur maximale atteint par une node du graph
		'''
		tt = self.tri_topologique()
		return len(tt)

	def longest_path(self, src : int, trg : int):
		''' 
		self	: open_digraph acyclique
		src		: int, id de node de départ
		trg		: int, id de node d'arrivée
		return	: ([int], int), le plus long chemin allant de src vers trg, ainsi que la longueur de ce chemin
		'''
		tt = self.tri_topologique()
		k = self.profondeur_node(src)	# Profondeur de la node d'arrivée.
										# Plus rapide de la recalculer directement que de passer par profondeur_node pour éviter a refaire le tri_topologique.
		if src not in self.nodes.keys():
			raise ValueError("Le départ n'est pas dans le graphe.")
		if trg not in self.nodes.keys():
			raise ValueError("L'arrivée n'est pas dans le graphe")

		dist = {src:0}
		prev = {}
		while k < len(tt):	# On va regarder toutes les profondeurs du tri topologique une a une, jusqu'a arriver a la dernière (len(tt))
			for w in tt[k]:
				for par in self.get_node_by_id(w).parents:
					if par in dist and ((w not in dist) or (w in dist and dist[w] < dist[par] + 1)): # Si aucun ancêtre de w est dans dist, src n'est pas ancêtre de w.
						dist[w] = dist[par] + 1
						prev[w] = par
				if w == trg: 	# On a trouvé le chemin le plus grand
					path = []	# De la même façon que pour shortest_path, on va venir rebrousser chemin
					cur = trg
					while cur != src:
						cur = prev[cur]
						path.append(cur)
					if cur in path:
						path.remove(cur)		# On considère que le chemin ne devrait pas contenir la src, donc on l'enlèvé ici.
					path = path[::-1] 			# Comme on a rebroussé chemin, le chemin trouvé est a l'envers donc on doit l'inverser.
					return (path, dist[trg]) 	# On a trouvé le résultat final dans cet étage
			k = k + 1	# On va a l'étage d'après

		raise Exception("Aucun chemin n'existe entre src et tgt.")
		return ([], -1) # Aucun chemin n'a été trouvé.

	def fusionne_node(self, a : int, b : int, new_label='') -> int:
		''' 
		a			: int, l'id du premier noeud de la fusion
		b			: int, l'id du second noeud de la fsion
		new_label	: [Optional] str, le label du noeud crée par la fusion (Sera le label de a si non spécifié)
		return		: int, l'id du noeud crée par la fusion
		Fusionne les deux noeuds dont les ids sont donnés en paramètre.
		En réalité, le noeud 'a' va 'absorber' le noeud b, càd que le noeud a va conserver toutes ses propriétée (Si c'est un input, un output et son label)
		Si b est un output et que a peut le devenir avec la fusion, alors le nouveau noeud sera un output. Idem pour les inputs.
		'''
		self.remove_parallel_edge(a, b)
		self.remove_parallel_edge(b, a)

		an = self.get_node_by_id(a)
		bn = self.get_node_by_id(b)
		# Les outputs et inputs ne sont plus dans le bon ordre
		if b in self.outputs and a not in self.inputs and a not in self.outputs and an.indegree() == 0:
			b_index = self.outputs.index(b)
			self.outputs[b_index] = a
		elif b in self.inputs and a not in self.outputs and a not in self.inputs and an.outdegree() == 0:
			b_index = self.inputs.index(b)
			self.inputs[b_index] = a

		for (un, deux) in bn.get_parents_ids().items():
			self.add_edge(un, a, deux)
		for (un, deux) in bn.get_children_ids().items():
			self.add_edge(a, un, deux)

		if new_label != '':
			an.set_label(new_label)
		
		self.remove_node_by_id(b) # On enlève b
		
		return a