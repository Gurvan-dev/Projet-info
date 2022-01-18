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

    @classmethod
    def empty():
        return open_digraph([], [], [])
