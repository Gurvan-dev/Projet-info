from modules.matrice import *
from random import randint

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
        self.inputs = inputs.copy()     # On réalise ici des copie afin d'être sûr d'éviter toute confusion pendant l'utilisation de la classe.
        self.outputs = outputs.copy()   # Une liste donnée en paramètre peut ainsi être ré-utilisée plus tard sans aucune incidence sur ce graphe.
        self.nodes = {node.id: node.copy() for node in nodes} # self.nodes: <int,node> dict
        if self.nodes == {}:    # On initialise ici un compteur qui va permettre d'avoir un ID unique pour chaque node,
            self.c = 0          # sans risque de ré-attribution d'un même id a plusieurs node,
        else:                   # et ce même après suppression ou ajout de plusieurs node. 
            self.c = max([node.id for node in nodes])

    def __str__(self) -> str:
        return f"Input : {self.inputs}   Output : {self.outputs}   Nodes : {[node for node in self.nodes]}"

    def __repr__(self):
        return f" Digraph({self})"

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes.values()) # On peut juste renvoyer un nouveau digraph avec comme paramètre les valeurs des variables actuels, car un copy est des le constructeur.

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
        '''
        label: Le nom de la node
        parents: Les parents de la node
        childrens : Les childrens de la node
        Ici les paramètres possèdent des noms plutôt explicite quant a leurs fonctions.
        Les parents ne seront pas directement ajouté a la node,
        mais seront plutôt utilisé comme argument pour faire des add_edge.
        De cette façon, on s'assure que le graphe soit bien formé qu'importe l'utilisation de add_node
        (Le seul moyen pour que le graphe soit mal formé étant ainsi une erreur)
        '''
        id = self.new_id()
        self.c = self.c + 1
        self.nodes[id] = node(id, label, {}, {})
        for p in parents:
            self.add_edge(p, id)
        for c in children:
            self.add_edge(id, c)
        return id

    def add_input_node(self, id):
        '''
        id: L'id sur laquelle greffer une nouvelle node qui sera une input node liée par une arrête a cette première.
        Throw une exception si la node sur laquelle on doit se greffer est elle même une input node, afin que le graphe reste bien formé.
        '''
        # Vérifier que id n'est pas un input !
        if id in self.inputs:
            raise Exception('Tentative d\'ajouter un input avant un input.')
        id_added = self.add_node()
        self.add_edge(id_added, id)
        self.inputs.append(id_added)

    def add_output_node(self, id):
        '''
        id: L'id sur laquelle greffer une nouvelle node qui sera une output node liée par une arrête a cette première.
        Throw une exception si la node sur laquelle on doit se greffer est elle même une output node, afin que le graphe reste bien formé.
        '''
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
        # Vérifier que la multiplicité est bien la même pour un parent et un enfant.
        for j in self.nodes.values():
            for i in j.get_children_ids().keys():
                if not i in self.nodes.keys():
                    return False
                n = self.get_node_by_id(i)
                if not (j.get_id() in n.get_parents_ids()) or j.get_children_ids()[i] != n.get_parents_ids()[j.get_id()]:
                    return False
        
        return True

    @classmethod
    def graph_from_adjacency_matrix(cls, self, mat):
        '''
        mat : int list list
        Return an open digraph formed with the input matrix (See sujets/TD3.pdf).
        '''
        o = open_digraph([], [], [])
        for i in range(len(mat)):
            o.add_node()
        for x in range(len(mat)):
            for y in range(len(may)):
                if mat[x][y] > 0:
                    o.add_edge(x, y) 
        return o

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form = "free"):
        '''
        Doc
        n       : Nombre de noeuds dans le graphe
        bound   : Nombre maximal de multiplicité pour une arrête
        inputs  : Nombre d'input a générer dans le graphe
        outputs : Nombre d'outputs a générer dans le graphe
        form :
            free                    : La matrice générée n'aura pas de contraintes.
            DAG                     : La matrice générée sera acyclique dirigé
            oriented                : La matrice sera orienté
            loop-free               : Un noeud ne pourra pas pointer sur lui même (Donc la diagonale de la matrice générée sera nulle)
            undirected              : La matrice sera symmétrique.
            loop-free undirected    : Combinaison de loop free et undirected
        '''

        if form=="free":
            mat = matrice.matrice.random_matrix(n, bound)
        elif form=="DAG":
            mat = matrice.matrice.random_matrix(n, bound, triagular=True)
        elif form=="oriented":
            mat = matrice.matrice.random_matrix(n, bound, oriented=True)
        elif form=="loop-free":
            o = graph_from_adjacency_matrix(mat, null_diag=True)
        elif form=="undirected":
            mat = matrice.matrice.random_matrix(n, bound, symmetric=True)
        elif form=="loop-free undirected":
            o = graph_from_adjacency_matrix(mat, symmetric=True ,null_diag=True)
        else:
            raise ValueError("Forme de matrice non correcte.")
            
        o = graph_from_adjacency_matrix(mat)

        inputs = max(input, n)
        outputs = max(outputs, n)

        for _ in range (inputs):
            r = randint(1, n+1)                   # Nos ID commencent a 1, d'ou le 1, n+1.
            while r in o.get_input_ids():         # Ne peut pas être une boucle infinie car on a restreint input a n au maximum
                r = (r+1) % (n+1)
            inputs.append(r)
            o.add_input_id(r)

        for _ in range (outputs):
            r = randint(1, n+1)                 # Nos ID commencent a 1, d'ou le 1, n+1.
            while r in get_outputs_ids:         # Ne peut pas être une boucle infinie car on a restreint output a n au maximum
                r = (r+1) % (n+1)
            outputs.append(r)
            o.add_output_id(r)
        
        return o

    def get_dic(self):
        '''
        return dictionnaire int -> int, associant a chaque id de noeud un unique entier 0 ≤ i < n
        '''
        dic = {}
        count = 0
        for nod in self.nodes.values():
            dic[nod.id] = count
            count = count + 1
        return dic

    def adjacency_matrix(self):
        '''
        return : La matrice d'adjacency associé au graph
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
