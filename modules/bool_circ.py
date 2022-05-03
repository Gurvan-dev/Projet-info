from modules.matrice import *
from modules.node import *
from modules.open_digraph import *
from random import randint, random, choice
from math import log
import os
import re
import sys

class bool_circ(open_digraph):

	def __init__(self, g):
		if isinstance(g, open_digraph):
			self.c = g.c
			self.inputs = g.inputs.copy()
			self.outputs = g.outputs.copy()
			self.nodes = g.nodes.copy()
		else:
			raise ValueError("Tentative de formation d'un circuit booléen avec un input n'étant pas un graph")
		if not self.is_well_formed():
			raise ValueError("Circuit Booléen mal formé")

	def __repr__(self) -> str:
		return f" BoolCirc({self})"

	def is_well_formed(self) -> bool:
		if self.is_cyclic():
			return False

		for node in self.nodes.values():
			if node.get_id() not in self.inputs and node.get_id() not in self.outputs:
				lab = node.get_label()
				if not (lab == '' or lab == ' ' or lab == '&' or lab == '|' or lab == '~' or lab == '0' or lab == '1' or lab == '^'): 	# Vérification que le label est valide
					return False
				if (lab == ' ' or lab == '') and (node.indegree() != 1 ): 													# Les portes de copies doivent avoir une seule entrée
					return False
				if (lab == '&' or lab=='|' or lab == '^') and (node.outdegree() != 1): 									# Les portes 'Et' et 'Ou' doivent avoir éxactement une sortie.
					return False      
				if (lab == '~') and (node.outdegree() != 1 or node.indegree() != 1): 						# Les portes 'Non' doivent avoir une entrée et une sortie.
					return False

		return True

	@classmethod
	def empty(cls):
		'''
		Return an empty bool digraph.
		'''
		return bool_circ(open_digraph.empty())


	@classmethod
	def from_string(cls, *args):
		''' 
		args		: des str, des formule propositionnelles de circuit booléen

		return		:	bool_circ, Renvoie le circuit booléen formé par la formule propositionelle 's'
		'''
		cls = bool_circ.empty()
		for s in args:	# Pour chacun des arguments, on va crée un nouveau graph puis le fusionner en parallèle de g
			
			g = bool_circ.empty()
			current_node = g.add_node()
			g.add_output_node(current_node)
			
			s2 = ''
			for c in s:
				cn = g.get_node_by_id(current_node)
				if c == '(':		
					if(cn.get_label() != s2):				# Si le label est déjà égal a s2, on évite d'avoir des problème du genre '&&' comme label
						cn.set_label(cn.get_label() + s2)
					current_node = g.add_node('', '', [current_node])
					s2 = ''
				elif c == ')':
					
					if(cn.get_label() != s2):				# Si le label est déjà égal a s2, on évite d'avoir des problème du genre '&&' comme label
						cn.set_label(cn.get_label() + s2)
					child = list(g.get_node_by_id(current_node).get_children_ids().keys())
					current_node = child[0]
					
					s2 = ''
				else :
					s2 += c
			cls.iparallel(g)	# On ajoute le graphe en parallèle de cls

		feuilles = []
		fusion_a_faire = {}
		for (id, n) in cls.nodes.items():		# On va regarder les feuilles (Ici les variables, les entrées)
			if len(n.get_parents_ids()) == 0:	# On vérifie si c'est bien une feuille
				feuilles.append(id)				# On va stocker toutes les feuilles
				cls.add_input_id(id)			# On les ajoute bien aux entrées du graphe

		for (id, n) in cls.nodes.items():		# On ajoute les queues aux outputs.
			if len(n.get_children_ids()) == 0:
				cls.add_outputs_id(id)

		for a in feuilles:			# Pour toutes les feuilles, on va regarder si il existe une autre feuille avec le même nom, i.e. que l'on peut fusionner
			for b in feuilles:
				if a != b and cls.get_node_by_id(a).get_label() == cls.get_node_by_id(b).get_label():	# Si a et b ont le même label (nom), on peut les fusionners
					ok = True
					for fus in fusion_a_faire.values():	# On vérifie que la fusion dans a et b n'est pas déjà stockée quelque part
						if a in fus and b in fus:
							ok = False

					if ok:	# Si la fusion n'est pas déjà stockée, on va regarder si a  ou b est déjà dans une liste de fusion a effectuer, auquel cas on ajoute ta ou b a la liste
						if a in fusion_a_faire and b not in fusion_a_faire[a]:									# Ici a est dans une fusion et b n'y est pas
							fusion_a_faire[a].append(b)
						elif a not in fusion_a_faire and b in fusion_a_faire and a not in fusion_a_faire[b]:	# Ici b est dans une fusion et a n'y est pas
							fusion_a_faire[b].append(a)
						elif a not in fusion_a_faire and b not in fusion_a_faire:								# Ici ni a ni b ne sont dans des fusions
							fusion_a_faire[a] = [b]

		for (a, bs) in fusion_a_faire.items():	# On effectue toutes les fusions a faire
			for b in bs:
				cls.fusionne_node(a, b)
		return bool_circ(cls)
	
	@classmethod
	def from_table(cls, strinput : str):
		"""
		strinput		: str, '0000110', dernière colonne du tableau. La taille du string doit être une puissance de 2.
		"""
		nombre_input = log(len(strinput), 2) 
		if nombre_input != int(nombre_input):
			raise ValueError("L'entrée n'est pas valide.")
		nombre_input = int(nombre_input)
		cls = bool_circ.empty()
		for i in range(nombre_input):
			an = cls.add_node()
			cls.add_input_id(an)
		
		f_list = []
		for i in range(len(strinput)): 					# Chaque ligne du tableau
			if(int(strinput[i]) != 0):
				table_a_ajouter = bin(i)[2:] 			# Correspond a la ligne du tableau associé a l'output
				etage = []
				for a in range(nombre_input): 			# Pour chaque colonne du tableau (Sauf output)
					if (a < len(table_a_ajouter) and table_a_ajouter[a] == 0) or a >= len(table_a_ajouter): # Si la table a la ligne i et colonne a est 0, alors on met la négation
						e = cls.add_node('~')																# Note : 0 également si out of bounds donc on le vérifie
						cls.add_edge(a, e)
						etage.append(e)
						
				f = cls.add_node('&')
				for e in etage:
					cls.add_edge(e, f)
				for inp in cls.get_input_ids():
					if inp not in etage:
						cls.add_edge(inp, f)
				f_list.append(f)
		
		big_ou = cls.add_node('|') # Le ou final
		out = cls.add_output_node(big_ou)
		for f in f_list:
			cls.add_edge(f, big_ou)
		
		return cls
	
	@classmethod
	def code_gray(cls, n : int):
		"""
		n		: int, > 1, le nombre de bit du code_gray
		return	: list(str), tout les nombre du code_gray codé sur n bit.
		"""
		if n < 1:
			raise ValueError("n ne peut pas être négatif")
		if n == 1:
			return ['0','1']
		fir = bool_circ.code_gray(n-1)
		cg = fir.copy()
		cg = cg[::-1]
		cls = []
		for c in fir:
			c = '0'+c
			cls.append(c)
		for c in cg:
			c = '1'+c
			cls.append(c)
		return cls
	
	@classmethod
	def K_map(cls, strinput : str):
		nb_input = int(log(len(strinput), 2))
		top = [i for i in range(0, int(nb_input /2))]
		bot = [i for i in range(int(nb_input/2), nb_input)] # bot peut contenir un élément de + que top si c'est impaire
		top_cg =  bool_circ.code_gray(len(top))
		bot_cg = bool_circ.code_gray(len(bot))
		cls = []
		for y in range(len(bot_cg)):
			line = []
			for x in range(len(top_cg)):
				res = 0
				## On doit chopper la ligne associée et la mettre dans res
				line_stat = int(f'{top_cg[x]}{top_cg[y]}', 2)
				
				line.append(strinput[line_stat])
			
			cls.append(line)
		print(top_cg)
		print(bot_cg)
		return cls

	@classmethod
	def random_bool(cls, n, inputs=1, outputs=1):
		""" 
		n		: int, le nombre de noeud dans le circuit booléen a produire
		inputs	: int, le nombre d'inputs présent dans le circuit booléen retourné
		outputs	: int,	/ pour le nombre d'outputs
		return	: bool_circ, un circuit booléen aléatoire avec les paramètres données
		"""
		if inputs < 1:
			raise(ValueError("Le nombre d'éntrée ne peut pas être inférieur à 1"))
		if outputs < 1:
			raise(ValueError("Le nombre de sortie ne peut pas être inférieur à 1"))
	
		cls = open_digraph.random(n, 1, form="DAG")

		for node in cls.get_nodes():
			if node.indegree() == 0:
				cls.add_input_node(node.get_id())

			if node.outdegree() == 0:
				cls.add_output_node(node.get_id())

		# Ajouter input ou output si nécéssaire
		diff_in = len(cls.get_input_ids()) - inputs
		diff_out = len(cls.get_output_ids()) - outputs		
		if diff_in > 0: # On a trop d'input
			# On remove un input diff_in fois, et on remplace l'input par un noeud de copie depuis un autre input
			# Comme le graphe est déjà aléatoire, en réalité on peut simplement retirer les diff_in premiers noeuds
			for i in range(diff_in):
				id = cls.inputs[0]
				rand = randint(diff_in - i, len(cls.inputs)-1)
				rand_id = cls.inputs[rand]
				cls.inputs.remove(id)
				cls.add_edge(rand_id, id)
				
		elif diff_in < 0: # Il nous manque des inputs!
			diff_in = -diff_in
			for i in range(diff_in):
				rand = randint(0,len(cls.nodes) - 1)
				rand_id = list(cls.nodes.keys())[rand]
				while rand_id in cls.get_input_ids() or rand_id in cls.get_output_ids():
					rand = randint(0,len(cls.nodes) - 1)
					rand_id = list(cls.nodes.keys())[rand]
				cls.add_input_node(rand_id)
		if diff_out > 0: # On a trop d'output
			# On remove un input diff_in fois, et on remplace l'input par un noeud de copie depuis un autre input
			# Comme le graphe est déjà aléatoire, en réalité on peut simplement retirer les diff_in premiers noeuds
			for i in range(diff_out):
				id = cls.outputs[0]
				rand = randint(diff_out - i, len(cls.outputs)-1)
				rand_id = cls.outputs[rand]

				cls.outputs.remove(id)
				cls.outputs.remove(rand_id)

				cls.add_edge(id, rand_id)
				cls.add_output_node(rand_id)
				
				
		elif diff_out < 0: # Il nous manque des outputs !
			diff_out = -diff_out
			for i in range(diff_out):
				rand = randint(0,len(cls.nodes) - 1)
				rand_id = list(cls.nodes.keys())[rand]
				while rand_id in cls.get_input_ids() or rand_id in cls.get_output_ids():
					rand = randint(0,len(cls.nodes) - 1)
					rand_id = list(cls.nodes.keys())[rand]
				cls.add_output_node(rand_id)
			

		for node in cls.get_nodes():
			if node.get_id() in cls.get_input_ids() or node.get_id() in cls.get_output_ids():
				continue
			if node.indegree() == 1 and node.outdegree() == 1: # Opérateur unaire
				node.set_label('~')
			elif node.indegree() == 1 and node.outdegree() > 1: # Noeud de copie
				pass
			elif node.indegree() > 1 and node.outdegree() == 1: # Opérateur binaire
				node.set_label(choice(['&', '|', '^']))
			else:
				uop = cls.add_node()
				ucp = cls.add_node()

				cls.add_edge(uop, ucp) 				# Il y ait une flêche de uop vers ucp
				for p in node.get_parents_ids(): 	# uop est pointé par tout les parents de u		
					cls.add_edge(p, uop)
				for c in node.get_children_ids():
					cls.add_edge(ucp, c)
				cls.remove_node_by_id(node.get_id())
				cls.get_node_by_id(uop).set_label(choice(['&', '|']))


		return cls

	@classmethod
	def adder(cls,taille : int):
		if(taille < 0):
			raise ValueError("La taille de l'Adder ne peut être négative.")
		elif(taille == 0):
			cls = bool_circ.empty()

			one = cls.add_node()
			two = cls.add_node()
			three = cls.add_node()

			cls.add_input_node(one)
			cls.add_input_node(two)
			cls.add_input_node(three)

			a = cls.add_node("&")

			cls.add_edge(one, a)
			cls.add_edge(two, a)

			b = cls.add_node("^")
			cls.add_edge(one, b)
			cls.add_edge(two, b)

			four = cls.add_node()
			cls.add_edge(b,four)
			
			c = cls.add_node("&")
			cls.add_edge(four, c)
			cls.add_edge(three, c)
			
			d = cls.add_node("^")
			cls.add_edge(three, d)
			cls.add_edge(four, d)
			
			e = cls.add_node("|")
			cls.add_edge(a,e)
			cls.add_edge(c,e)

			
			cls.add_output_node(e)
			cls.add_output_node(d)

		else:
			
			cls = bool_circ.adder(taille-1)
			A2 = bool_circ.adder(taille-1)
			cls.iparallel(A2)
			retenueA1_in = A2.outputs.pop(0)
			retenueA1 = cls.inputs[len(cls.inputs) - len(A2.inputs) -1]
			cls.add_edge(retenueA1_in, retenueA1)
			cls.outputs.remove(retenueA1_in)
			cls.inputs.remove(retenueA1)

			
			# On va ré-organiser les inputs pour correspondre a l'addition.
			# Cette méthode est moins lisible que d'autre quand on essaye de faire un .display(),
			# Mais marche tout aussi bien en gardant un code compact
			taille_moit = (int)(len(A2.inputs)-1) 
			new_inp = []
			part1 = cls.inputs[:taille_moit]
			part2 = A2.inputs
			taille_moit2 = int(taille_moit/2)
			for i in part1[:taille_moit2]:
				new_inp.append(i)
			for i in part2[:taille_moit2]:
				new_inp.append(i)
			for i in part1[taille_moit2:]:
				new_inp.append(i)
			for i in part2[taille_moit2:]:
				new_inp.append(i)

			print(f"inp {part1} {part2} {new_inp}")
			cls.set_input_ids(new_inp)
			return cls
			for i in range(taille_moit):
				new_inp.append(cls.inputs[2*i])
			for i in range(taille_moit):
				new_inp.append(cls.inputs[(2*i)+1])
			new_inp.append(cls.inputs[-1]) # On garde la retenue dans les inputs
			cls.set_input_ids(new_inp)
			
		
		return cls

	@classmethod
	def half_adder(cls, taille : int):
		cls = bool_circ.adder(taille)
		added = cls.add_node("0")
		retenue_id = cls.inputs[len(cls.inputs) -1]
		retenue_node =cls.get_node_by_id(retenue_id)
		for child in retenue_node.children:
			for _ in range(retenue_node.get_children_mult(child)):
				cls.add_edge(added, child)
		cls.remove_node_by_id(retenue_id)
		return cls

	@classmethod
	def registre(cls, entier : int, taille:int):
		'''
		return : bool_circ, représente l'entier en binaires
		'''
		cls = bool_circ.empty()
		bin_str = bin(entier)[2:]
		diff = taille - len(bin_str)
		if diff > 0:
			for _ in range(diff):
				added = cls.add_node(label='0')
				cls.add_output_node(added)
		if diff < 0:
			bin_str = bin_str[abs(diff):]
		for lab in bin_str:
			added = cls.add_node(label=lab)
			cls.add_output_node(added)
		return cls

	def transformation_non(self, par : int, enf : int) -> bool:
		''' 
		par		: int, l'id d'une note 1 ou 0
		enf		: int, l'id d'une node enfant de par avec label '~'
		return	: bool, vrai si la transformation a pu être éffécutée et faux sinon
		'''
		enf_node = self.get_node_by_id(enf)
		par_node = self.get_node_by_id(par)
		if enf_node.get_label() != '~' or (par_node.get_label() != '0' and par_node.get_label() != '1') or (par not in enf_node.get_parents_ids()):
			return False
		lab = par_node.get_label()
		new = self.fusionne_node(par, enf)
		if lab == '0':
			lab = '1'
		else:
			lab = '0'
		# Pas besoin de retirer les parents ici car il ne devrait pas y en avoir
		new_node = self.get_node_by_id(new)
		new_node.set_label(lab)
		return True

	def transformation_copie(self, par : int, enf : int) -> bool:
		''' 
		par		: int, l'id d'une note 1 ou 0
		enf		: int, l'id d'une node enfant de par avec label '~'
		return	: bool, vrai si la transformation a pu être éffécutée et faux sinon
		'''
		enf_node = self.get_node_by_id(enf)
		par_node = self.get_node_by_id(par)
		
		if enf_node.get_label() != '' or (par_node.get_label() != '0' and par_node.get_label() != '1') or (par not in enf_node.get_parents_ids()):
			return False
		
		lab = par_node.get_label()
		for child_of_enf in enf_node.get_children_ids():
			new = self.add_node(lab)
			self.add_edge(new, child_of_enf)
		self.remove_node_by_id(par)
		self.remove_node_by_id(enf)
		
		return True

	def transformation_et(self, par : int, enf : int) -> bool:
		''' 
		par		: int, l'id d'une note 1 ou 0
		enf		: int, l'id d'une node enfant de par avec label '~'
		return	: bool, vrai si la transformation a pu être éffécutée et faux sinon
		'''
		enf_node = self.get_node_by_id(enf)
		par_node = self.get_node_by_id(par)
		if enf_node.get_label() != '&' or (par_node.get_label() != '0' and par_node.get_label() != '1') or (par not in enf_node.get_parents_ids()):
			return False
		lab = par_node.get_label()
		new = self.fusionne_node(par, enf)
		if lab == '0': # Si c'est un 0, alors la porte vaut forcément zéro
			lab = '0'
			self.remove_all_parents(new)
		else: # Si c'est un 1, ça dépend de la deuxième entrée
			lab = ''
		new_node = self.get_node_by_id(new)
		new_node.set_label(lab)
		return True

	def transformation_ou_exclusif(self, par : int, enf : int) -> bool:
		''' 
		par		: int, l'id d'une note 1 ou 0
		enf		: int, l'id d'une node enfant de par avec label '~'
		return	: bool, vrai si la transformation a pu être éffécutée et faux sinon
		'''
		enf_node = self.get_node_by_id(enf)
		par_node = self.get_node_by_id(par)
		if enf_node.get_label() != '^' or (par_node.get_label() != '0' and par_node.get_label() != '1') or (par not in enf_node.get_parents_ids()):
			return False
		lab = par_node.get_label()
		new = self.fusionne_node(par, enf)
		if lab == '0':
			lab = ''
		else:
			lab = '~'
		
		new_node = self.get_node_by_id(new)
		new_node.set_label(lab)
		return True


	def transformation_ou(self, par : int, enf : int) -> bool:
		''' 
		par		: int, l'id d'une note 1 ou 0
		enf		: int, l'id d'une node enfant de par avec label '~'
		return	: bool, vrai si la transformation a pu être éffécutée et faux sinon
		'''
		enf_node = self.get_node_by_id(enf)
		par_node = self.get_node_by_id(par)
		if enf_node.get_label() != '|' or (par_node.get_label() != '0' and par_node.get_label() != '1') or (par not in enf_node.get_parents_ids()):
			return False
		lab = par_node.get_label()
		new = self.fusionne_node(par, enf)
		if lab == '0':
			lab = ''
		else:
			lab = '1'
			self.remove_all_parents(new)
		
		new_node = self.get_node_by_id(new)
		new_node.set_label(lab)
		return True

	# TEMP
	def cofeuille(self):
		cof = []
		for i in self.nodes:
			i_node = self.get_node_by_id(i)
			if i_node.indegree() == 0:
				cof.append(i)
		return cof

	def evaluate(self):
		# On va temporairement faire une méthode peut optimiser qui consiste a bruteforce absolument tout
		modif = True
		while modif:
			modif = False
			for n_id in self.cofeuille():
				if not modif:
					n_node = self.get_node_by_id(n_id)
					
					if n_node.indegree() == 0 and n_node.outdegree() > 0: # On tiens une co-feuille ! Normallement c'en est forcément une lol
						n_child = list(n_node.get_children_ids())[0]	
						if n_child not in self.outputs:	
							if self.transformation_copie(n_id, n_child):
								modif = True
							elif self.transformation_et(n_id, n_child):
								modif = True
							elif self.transformation_non(n_id, n_child):
								modif = True
							elif self.transformation_ou(n_id, n_child):
								modif = True
							elif self.transformation_ou_exclusif(n_id, n_child):
								modif = True
			

