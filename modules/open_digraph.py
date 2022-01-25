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
        return f"   Id : {self.id}\n   Label : {self.label}\n   Parents : {self.parents}\n   Children : {self.children}"

    def __repr__(self):
        return f" Node({self})"

    def copy(self):
        return node(self.identity, self.label, self.parents, self.children)
    
    def get_id(self):
        return self.id

    def get_label(self):
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

    def add_parent_id(self, parent_id, mult):
        self.parents[parent_id] = mult

    def add_children_id(self, child_id, mult):
        self.children[child_id] = mult
    


class open_digraph:  # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}

    def __str__(self) -> str:
        return f"  Input : {self.inputs} \n  Output : {self.outputs} \n  Nodes : {[id for id in self.nodes]}"

    def __repr__(self):
        return f" Digraph({self})"

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes)

    def new_id(self):
        return len(self.nodes) + 1

    @classmethod
    def empty():
        return open_digraph([], [], [])

    def get_input_ids(self):
        return self.inputs

    def get_output_ids(self):
        return self.outputs
    
    def get_id_node_map(self):
        return self.nodes

    def get_nodes(self):
        return [nodu for i, nodu in self.nodes]

    def get_nodes_ids(self):
        return [i for i, nodu in self.nodes]
    
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

    def add_edge(self, src, trg):
        self.get_node_by_id(src).children.add(trg)