class node:
	def __init__(self, identity, label, parents, children):
		'''
		identity: int; its unique id in the graph
		label: string;
		parents: int->int dict; maps a parent node's id to its multiplicity
		children: int->int dict; maps a child node's id to its multiplicity
		'''
		self.id = identity
		self.label = label
		self.parents = parents.copy()
		self.children = children.copy()

	def __str__(self) -> str:
		return f"Id : {self.id}   Label : {self.label}   Parents : {self.parents}   Children : {self.children}"

	def __repr__(self) -> str:
		return f" Node({self})"

	def __eq__(self, other) -> bool:
		# Pour le coup sort ici n'est pas opti mais permet de s'éviter des casse tête dans la formation des graphes.
		self.sort()
		other.sort()
		return self.id == other.id and self.label == other.label and self.children == other.children and self.parents == other.parents

	def sort(self):
		self.children = sorted(self.children)
		self.parents = sorted(self.parents)

	def copy(self):
		return node(self.id, self.label, self.parents, self.children)
	
	def get_id(self) -> int:
		return self.id

	def get_label(self) -> str:
		return self.label

	def get_parents_ids(self):
		return self.parents

	def get_children_ids(self):
		return self.children

	def get_children_mult(self, id):
		'''
		Retourne la multiplicité de id
		'''
		return self.children[id]

	def get_parent_mult(self, id):
		return self.parents[id]

	def set_id(self, new_id):
		self.id = new_id

	def set_parent_ids(self, new_parent):
		self.parents = new_parent

	def set_childen_ids(self, new_ids):
		self.children = new_ids
	
	def set_label(self, new_label):
		self.label = new_label

	def add_parent_id(self, parent_id, mult = 1):
		if self.parents.get(parent_id) == None:
			self.parents[parent_id] = mult
		else:
			self.parents[parent_id] += mult

	def add_children_id(self, child_id, mult = 1):
		if self.children.get(child_id) == None:
			self.children[child_id] = mult
		else:
			self.children[child_id] += mult

	def remove_parent_once(self, id):
		if id in self.parents:
			self.parents[id] -= 1
			if self.parents[id] == 0:
				self.parents.pop(id)

	def remove_child_once(self, id):
		if id in self.children:
			self.children[id] -= 1
			if self.children[id] == 0:
				self.children.pop(id)

	def remove_parent_id(self, id):
		self.parents.pop(id)

	def remove_child_id(self, id):
		self.children.pop(id)
	
	def indegree(self):
		return sum(self.parents.values())
		
	def outdegree(self):
		return sum(self.children.values())
	
	def degree(self):
		return self.indegree + self.outdegree
	
	def shift_indice(self, shiftInd):
		pc = {}
		cc = {}
		for id in self.parents.keys():
			pc[id+shiftInd] = self.parents[id]
		for id in self.children.keys():
			cc[id+shiftInd] = self.children[id]
		self.parents=pc
		self.children=cc
