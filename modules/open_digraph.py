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
        return self.id == other.id and self.label == other.label and self.children == other.children and self.parents == other.parents

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

    def set_id(self, new_id):
        self.id = new_id

    def set_parent_ids(self, new_parent):
        self.parents = new_parent

    def set_childen_ids(self, new_ids):
        self.children = new_ids

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



class open_digraph:  # for open directed graph
    def __init__(self, inputs=[], outputs=[], nodes=[]):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        self.nodes = {node.id: node.copy() for node in nodes} # self.nodes: <int,node> dict
        if self.nodes == {}:
            self.c = 0
        else:
            self.c = max([node.id for node in nodes])

    def __str__(self) -> str:
        return f"Input : {self.inputs}   Output : {self.outputs}   Nodes : {[id for id in self.nodes]}"

    def __repr__(self):
        return f" Digraph({self})"

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes.values())

    def __eq__(self, __o: object) -> bool:
        return self.inputs == object.inputs and object.outputs == object.outputs and self.nodes == object.nodes and self.c == object.c 

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
    
    def get_node_by_id(self, i):
        return self.nodes[i]

    def get_nodes_by_ids(self, t):
        res = []
        for i in t:
            res.append(self.nodes[i])
        return res

    def set_input_ids(self, ids):
        self.inputs = ids
    
    def set_output_ids(self, ids):
        self.outputs = ids

    def add_input_id(self, id):
        self.inputs.append(id)

    def add_outputs_id(self, id):
        self.outputs.append(id)

    def new_id(self):
        return self.c + 1

    def add_edge(self, src, trg):
        self.get_node_by_id(src).add_children_id(trg)
        self.get_node_by_id(trg).add_parent_id(src)
    
    def add_edges(self, edgeList):
        for (src, trg) in edgeList:
            self.add_edge(src,trg)
    
    def add_node(self, label='', parents={}, children={}):
        id = self.new_id()
        self.c = self.c + 1
        # TODO : Utiliser add edge ici
        self.nodes[id] = node(id, label, parents, children)
        return id

    def add_input_node(self, id):
        # Vérifier que id n'est pas un input !
        if id in self.inputs:
            raise Exception('Tentative d\'ajouter un input avant un input.')
        id_added = self.add_node()
        self.add_edge(id_added, id)
        self.inputs.append(id_added)

    def add_output_node(self, id):
        # Vérifier que id n'est pas un output !
        if id in self.outputs:
            raise Exception('Tentative d\'ajouter un output derrière un output.')
        id_added = self.add_node()
        self.add_edge(id, id_added)
        self.outputs.append(id_added)


    def remove_edge(self, src, trg):
        self.get_node_by_id(trg).remove_parent_once(src)
        self.get_node_by_id(src).remove_child_once(trg)

    def remove_parallel_edge(self, src, trg):
        self.get_node_by_id(trg).remove_parent_id(src)
        self.get_node_by_id(src).remove_child_id(trg)

    def remove_node_by_id(self, id):
        n = self.nodes.pop(id)
        for p in n.get_parents_ids():
            if p in self.nodes:
                self.get_node_by_id(p).remove_child_id(n.get_id())
        for c in n.get_children_ids():
            if c in self.nodes:
                self.get_node_by_id(c).remove_parent_id(n.get_id())

    def remove_edges(self, listEdge):
        for (src, trg) in listEdge:
            self.remove_edge(src, trg)

    def remove_parallel_edges(self, listEdge):
        for (src, trg) in listEdge:
            self.remove_parallel_edge(src, trg)

    def remove_nodes_by_id(self, ids):
        for id in ids:
            self.remove_node_by_id(id)

    def is_well_formed(self):
        for n in self.inputs:
            if not (n in self.nodes): # Vérifier que tout les éléments d'input sont dans le graphe.
                return False
            if len(self.get_node_by_id(n).get_children_ids()) != 1: # Vérifier que les inputs n'ont qu'un enfant
                return False 
            if len(self.get_node_by_id(n).get_parents_ids()) > 1: # Vérifier que les inputs n'ont pas de parents
                return False 
        for n in self.outputs:
            if not (n in self.nodes): 
                return False
            if len(self.get_node_by_id(n).get_parents_ids()) != 1: # Vérifier que les outputs n'ont qu'un parent
                return False 
            if len(self.get_node_by_id(n).get_children_ids()) > 0: # Vérifier que les outputs n'ont pas d'enfants
                return False
        for key in self.nodes.keys():
            if(self.get_node_by_id(key).get_id() != key): # Vérifier que les cléfs de nodes correspondent a l'id.
                return False
        # TODO : si j a pour fils i avec multiplicit ́e m, alors i doit avoir pour parent j avec multiplicit ́e m, et vice-versa
        for j in self.nodes.values():
            for i in j.get_children_ids().keys():
                if not i in self.nodes.keys():
                    return False
                n = self.get_node_by_id(i)
                if not (j.get_id() in n.get_parents_ids()) or j.get_children_ids()[i] != n.get_parents_ids()[j.get_id()]:
                    return False
        
        return True