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
        self.parents = parents
        self.children = children

    def __str__(self) -> str:
        return f"Id : {self.id}   Label : {self.label}   Parents : {self.parents}   Children : {self.children}"

    def __repr__(self) -> str:
        return f" Node({self})"

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.label == other.label and self.children == other.children and self.parents == other.parents

    def copy(self):
        return node(self.identity, self.label, self.parents, self.children)
    
    def get_id(self) -> int:
        return self.id

    def get_label(self) -> str:
        return self.label

    def get_parents_ids(self):
        return self.parents

    def get_children_id(self):
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

    def remove_children_once(self, id):
        if id in self.children:
            self.children[id] -= 1
            if self.children[id] == 0:
                self.children.pop(id)

    def remove_parent_id(self, id):
        self.parents.pop(id)

    def remove_child_id(self, id):
        self.children.pop(id)



class open_digraph:  # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes} # self.nodes: <int,node> dict
        self.c = 0

    def __str__(self) -> str:
        return f"Input : {self.inputs}   Output : {self.outputs}   Nodes : {[id for id in self.nodes]}"

    def __repr__(self):
        return f" Digraph({self})"

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes)

    @classmethod
    def empty():
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
        self.get_node_by_id(src).add_parent_id(trg)
        self.get_node_by_id(trg).add_children_id(trg)
    
    def add_node(self, label='', parents={}, children={}):
        id = self.new_id()
        self.c = self.c + 1
        self.nodes[id] = node(id, label, parents, children)

    def remove_edge(self, src, trg):
        self.get_node_by_id(src).remove_parent_once(trg)
        self.get_node_by_id(trg).remove_children_once(trg)

    def remove_parallel_edge(self, src, trg):
        self.get_node_by_id(src).remove_parent(trg)
        self.get_node_by_id(src).remove_children(trg)

    def remove_node_by_id(self, id):
        n = self.nodes.pop(id)

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
        for n in input:
            if not (n in self.nodes): # Vérifier que tout les éléments d'input sont dans le graphe.
                return False
            if len(self.get_node_by_id(n).get_children_ids()) != 1: # Vérifier que les inputs n'ont qu'un enfant
                return False 
            if len(self.get_node_by_id(n).get_parents_ids()) > 1: # Vérifier que les inputs n'ont pas de parents
                return False 
        for n in output:
            if not (n in self.nodes): 
                return False
            if len(self.get_node_by_id(n).get_parents_ids() != 1): # Vérifier que les outputs n'ont qu'un parent
                return False 
            if len(self.get_node_by_id(n).get_children_ids()) > 0: # Vérifier que les outputs n'ont pas d'enfants
                return False
        for key in self.nodes.keys():
            if(self.get_node_by_id(no).get_id() != key): # Vérifier que les cléfs de nodes correspondent a l'id.
                return False
        # TODO : si j a pour fils i avec multiplicit ́e m, alors i doit avoir pour parent j avec multiplicit ́e m, et vice-versa
        
        return True