#AI class
import copy
import math
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
        
        while puzzle.get_move_from_state(state) != "0-0":
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
        winningstate = self.AStarSearch(self.puzzle.state)
        self.puzzle = copy.deepcopy(self.saved_puzzle_move) 
        return [] 
    def AStarSearch(self,startState):
        closedNodes = {}
        openNodes = [[startState , 0]]
        cameFrom = [[startState,None]]
        
        gScore = [[startState,0]]
        #cameFrom[startState] = None
        #gScore[startState] = 0
        
        clean_puzzle = copy.deepcopy(self.puzzle)
        
        while len(openNodes) != 0:
            current = openNodes.pop(0)[0]
        
            self.puzzle = copy.deepcopy(clean_puzzle)                    
            if self.puzzle.get_move_from_state(current) != "0-0":           
                temp_moves = AI.move_find_path_of_state(self,current,self.puzzle)
                for move in temp_moves:
                    self.puzzle.make_a_move(move,1,1)
                for c_node in self.puzzle.state_tree.get_leaf_nodes(self.puzzle.state_tree.get_node_of_state(self.puzzle.state)):
                    self.ai_tree.add_node(c_node,current)  
                print(ai_tree)
                self.puzzle = copy.deepcopy(clean_puzzle)                        
            if self.puzzle.is_goal_match(current):
                break
            for nextnode in self.ai_tree.get_leaf_nodes(self.ai_tree.get_node_of_state(current)):
                new_cost = AStarAI.find_value(gScore,current) + self.puzzle.get_cost(nextnode.state)
                if nextnode.state not in AStarAI.find_all_states(gScore) or new_cost < find_value(gScore,nextnode.state):
                    gScore.append([nextnode.state, new_cost])
                    priority = new_cost + self.puzzle.heuristic(0)
                    openNodes.append([nextnode.state,priority])
                    cameFrom.append([nextnode.state,current])
                    
        return [cameFrom,gScore]
    
    def find_value(clist,state):
        for index in range(0,len(clist)):
            if clist[index][0]== state:
                return clist[index][1]
    def find_all_states(clist):
        ret = []
        for item in clist:
            ret.append(item[0])
        return ret