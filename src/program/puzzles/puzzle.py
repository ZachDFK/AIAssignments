#puzzle Class

from abc import ABC, abstractmethod
class Puzzle():
    
    movestates = []
    logofmoves = []

    
    @abstractmethod
    def update_states():
        pass
    
    @abstractmethod 
    def is_over():
        pass
    
    @abstractmethod
    def make_a_move():
        pass
    @abstractmethod
    def is_goal_match(state):
        pass
    @abstractmethod
    def log_move(state):
        pass
    
    def print_move(str):
        print(str)
    
    def get_moves():
        return movestates
    def print_log_moves(self):
        for log in self.logofmoves:
            Puzzle.print_move(log)
            
class StateTreeNode:
        
    
    def __init__(self,state,root=None):
        self.root = root
        self.state = state
    def get_state(self):
        return self.state
    def get_move(self):
        return self.state[4]
    def get_root(self):
        return self.root
    
    def get_height(self,height=0):
        if(self.root == None or self.root == 0):
            return height
        else:
            height +=1
            return self.root.get_height(height)
    
class StateTree:
    def __init__(self,init_state):
        self.baseroot = StateTreeNode(init_state)
        self.nodes = [self.baseroot]
    def add_node(self,node,root=None):
        if(root == None):
            node.root = self.baseroot
        else:
            node.root = root
            self.nodes.append(node)
    def get_nodes_of_level(self,level):
        l_nodes = []
        for node in self.nodes:
            if node.get_height() == level:
                l_nodes.append(node)
        return l_nodes
    def get_leaf_nodes(self,bnode=None):
        if bnode == None:
            bnode = self.baseroot
        l_nodes = []
        for node in self.nodes:
            if(node.root == bnode):
                l_nodes.append(node)
        return l_nodes
    def get_node_of_state(self,state):
        for node in self.nodes:
            if node.state == state:
                return node
            
        print("What?")
        return 0
    def __str__(self):
        tstr = ""
        for node in self.nodes:
            if node == int:
                print("bug here")
            tstr += "State: " + str(node.state) + " level: " + str(node.get_height()) + "\n"
        return tstr
        