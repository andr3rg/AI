
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent): 
        self.state = state
        self.parent = parent
        self.depth = parent.depth+1 if parent != None else 0
        self.cost =self.parent.cost if self.parent != None else 0
        self.heuristic=0
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.length = 0
        self.limit=0    
        self.Count=0
        self.fathers=-1
        self.non_terminals=0
        self.avg_branching=0
        self.terminals=0
        self.cost=0

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self,limit=None):
        if limit != None:
            self.limit = limit
        else: limit=0
        
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            
            if self.problem.goal_test(node.state):
                self.solution = node
                self.length = self.solution.depth if self.solution != None else None

                self.terminals= self.Count -(self.fathers)   #counting the number of terminals nodes
                self.non_terminals=self.fathers +1  #root node is not a terminal node

                self.avg_branching=(self.Count)/self.non_terminals  #average branching factor
                self.cost= node.cost
                return self.get_path(node)
            
            
            lnewnodes = []
            

            self.fathers+=1 #counting the number of fathers

            for a in self.problem.domain.actions(node.state):# para cada accao
                 
                newstate = self.problem.domain.result(node.state,a) # calcular o novo estado
                newnode = SearchNode(newstate,node) # criar um novo no com esse estado
               
                newnode.cost += self.problem.domain.cost(node.state,a) # calcular o custo do novo no

                lnewnodes.append(newnode) #
                newnode.heuristic=self.problem.domain.heuristic(newnode.state,self.problem.goal) #simulate path cost
                if newnode.parent == None:  # se o novo no for a raiz   
                    continue        
                if newnode.state in self.get_path(node):# se o novo no ja estiver no caminho ate ao no actual
                    lnewnodes.remove(newnode) 
                    continue       # descarta o no


                if self.strategy=='depth':   
                    if newnode.depth > self.limit and self.limit != 0:
                        lnewnodes.remove(newnode)

                    continue    
                
            self.Count+= len(lnewnodes) #counting the number of nodes
            self.add_to_open(lnewnodes)
            if self.strategy=='greedy':
                self.open_nodes.sort(key=lambda node: node.heuristic) #ordena os novos nos por ordem de custo simulado
                i=0
                store=[]
                for nos in self.open_nodes:
                    i +=1
                    if i==1:
                        continue
                    else:
                        store.append(nos)
                        self.open_nodes.remove(nos)

            
                           
            
            if self.strategy=='uniform':
                self.open_nodes.sort(key=lambda node: node.cost)  #ordena os novos nos por ordem crescente de custo
            
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes) 
        elif self.strategy == 'depth': 
            self.open_nodes[:0] = lnewnodes 
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)  
            pass

@property 
def depth (self):
    return (self.depth)

@property 
def length (self):
    return (self.lenght)
@property  
def avg_branching(self):
    return (self.Count/self.Fathers+1)
@property
def cost(self):
    return (self.cost)