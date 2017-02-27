#AI class
import copy
import sys
from ..puzzles import transpuzzle,spacepuzzle
class AI:


    def __init__(self,puzzle,style):
        self.activepuzzle = puzzle
        self.style = style
        self.real_ai = self.set_ai(style)
        
    def set_ai(self,style):
        if style == "Breadth First":
            real_ai = BreadthFirstAI(self.activepuzzle)
        elif style == "Depth First":
            real_ai = DepthFirstAI(self.activepuzzle)
        else:
            real_ai = AStarAI(self.activepuzzle)
        return real_ai

    def move_find_path_of_state(sai,state,puzzle):
        listofmoves = []
        
        while puzzle.get_move_from_state(state) != "default":
            listofmoves.insert(0,puzzle.get_move_from_state(state))
            state = sai.ai_tree.get_node_of_state(state).root.state
        return listofmoves
        
        
class BreadthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.first_in_first_out(0)
        self.puzzle = copy.deepcopy(self.saved_puzzle_move)        
        return AI.move_find_path_of_state(self,winningstate,self.puzzle)
        
    def first_in_first_out(self,level):
        #print(self.ai_tree)
        if self.puzzle.is_goal_match():
            return self.puzzle.state
        else:
            clean_puzzle = copy.deepcopy(self.puzzle)
            level +=1
            for node in self.ai_tree.get_nodes_of_level(level):
            
                self.puzzle = copy.deepcopy(clean_puzzle)                  
                temp_moves = AI.move_find_path_of_state(self,node.state,self.puzzle)
                print(temp_moves)
                for move in temp_moves:
                    self.puzzle.make_a_move(move,1,1)
                if self.puzzle.is_goal_match():                       
                    return node.state      
                
                for c_node in self.puzzle.state_tree.get_leaf_nodes(self.puzzle.state_tree.get_node_of_state(self.puzzle.state)):
                    self.ai_tree.add_node(c_node,node)
                
                self.puzzle = copy.deepcopy(clean_puzzle)
                   
            return self.first_in_first_out(level)
class DepthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.depth_search(0)
        self.puzzle = copy.deepcopy(self.saved_puzzle_move)
    
        return AI.move_find_path_of_state(self,winningstate,self.puzzle)
    def depth_search(self,level):
        if self.puzzle.is_goal_match():
            return self.puzzle.state
        else:
            clean_puzzle = copy.deepcopy(self.puzzle)
            level +=1
            for node in self.ai_tree.get_nodes_of_level(level):
                self.puzzle = copy.deepcopy(clean_puzzle)                  
                temp_moves = AI.move_find_path_of_state(self,node.state,self.puzzle)
                print(temp_moves)
                for move in temp_moves:
                    self.puzzle.make_a_move(move,1,1)
                if self.puzzle.is_goal_match():
                    return node.state
                for c_node in self.puzzle.state_tree.get_leaf_nodes(self.puzzle.state_tree.get_node_of_state(self.puzzle.state)):
                    self.ai_tree.add_node(c_node,node)
                
                self.puzzle = copy.deepcopy(clean_puzzle)
                return self.depth_search(level)
class AStarAI():
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.AStarSearch(self.ai_tree.get_nodes_of_level(0)[0])
        self.puzzle = copy.deepcopy(self.saved_puzzle_move) 
        
        return  AI.move_find_path_of_state(self,winningstate,self.puzzle)
    def AStarSearch(self,startNode):
        self.closedNodes = []
        self.openNodes = [startNode]
        self.heur = self.puzzle.heuristic(1,startNode)
        self.g_score = dict()
        self.g_score.setdefault("default",["default",sys.maxsize])
        self.f_score = dict()
        self.f_score.setdefault("default",["default",sys.maxsize])
        self.g_score[startNode] = [startNode.state,0]
        self.f_score[startNode] = [startNode.state,self.heur]
        #cameFrom[startState] = None
        #costSoFar[startState] = 0
        
        clean_puzzle = copy.deepcopy(self.puzzle)
        winning_Node = startNode
        while len(self.openNodes) != 0:
            current = self.get_state_with_lowest_f_score()
            
            if self.puzzle.is_goal_match(current.state):
                return current.state            
            
            self.puzzle = copy.deepcopy(clean_puzzle)                    
            if self.puzzle.get_move_from_state(current.state) != "default":           
                temp_moves = AI.move_find_path_of_state(self,current.state,self.puzzle)
                for move in temp_moves:
                    self.puzzle.make_a_move(move,1,1)
                for c_node in self.puzzle.state_tree.get_leaf_nodes(self.puzzle.state_tree.get_node_of_state(self.puzzle.state)):
                    self.ai_tree.add_node(c_node,self.ai_tree.get_node_of_state(current.state))  
                self.heur = self.puzzle.heuristic(1,current)
                #print(self.ai_tree)
                self.puzzle = copy.deepcopy(clean_puzzle)                        
            
            
            self.openNodes.remove(current)
            self.closedNodes.append(current)
            for nextnode in self.ai_tree.get_leaf_nodes(self.ai_tree.get_node_of_state(current.state)):
                
                if nextnode.state in AStarAI.get_states(self.closedNodes):
                    continue
                tentative_g_score = self.g_score[current][1] + self.puzzle.distance(current.state,nextnode.state)
                if nextnode.state not in AStarAI.get_states(self.openNodes):
                    self.openNodes.append(nextnode)
                elif tentative_g_score >= AStarAI.find_g_score_equivalent(nextnode,self.g_score):
                    continue
                self.g_score[nextnode] = [nextnode.state,tentative_g_score]
                self.f_score[nextnode] = [nextnode.state,self.g_score[nextnode][1] + self.heur]
            
            AStarAI.print_states_nodes(self.openNodes)
            AStarAI.print_states_nodes(self.closedNodes)            
        return "Error"
    
    def find_value(clist,state):
        for index in range(0,len(clist)):
            if clist[index][0]== state:
                return clist[index][1]
    def find_all_states(clist):
        ret = []
        for item in clist:
            ret.append(item[0])
        return ret
    def get_state_with_lowest_f_score(self):
        lowest_score = self.f_score.get("default")[1]
        result_node = None
        for node in self.openNodes:
            potential_cost = self.f_score[node][1]
            if lowest_score > potential_cost:
                lowest_score = potential_cost
                result_node = node
             
            
        return result_node
    def get_states(Nodes):
        lis = []
        for node in Nodes:
            lis.append(node.state)
        return lis
    def find_g_score_equivalent(node,g_score):
        for key in iter(g_score):
            if node.state == g_score.get(key)[0]:
                return g_score.get(key)[1]
    def print_states_nodes(nodes):
        strg = ""
        for node in nodes:
            strg += str(node.state) + "\n"
        print(strg + "\n")