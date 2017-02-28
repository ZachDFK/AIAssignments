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

    def move_find_path_of_state(sai,node,puzzle):
        listofmoves = []
        while puzzle.get_move_from_state(node.state) != "default":
            
            listofmoves.insert(0,puzzle.get_move_from_state(node.state))
            node = node.root
        return listofmoves
        
    def backtracker(ai,current,heuristic_type = None):
        
        ai.puzzle = copy.deepcopy(ai.clean_puzzle)                    
        if ai.puzzle.get_move_from_state(current.state) != "default":           
            print("State: " + str(current.state))
            temp_moves = AI.move_find_path_of_state(ai,current,ai.puzzle)
            for move in temp_moves:
                ai.puzzle.make_a_move(move,1,1)
            for c_node in ai.puzzle.state_tree.get_leaf_nodes(ai.puzzle.state_tree.get_node_of_state(ai.puzzle.state)):
                ai.ai_tree.add_node(c_node,ai.ai_tree.get_node_of_state(current.state))  
            if heuristic_type != None:
                ai.heur = ai.puzzle.heuristic(heuristic_type,current)
            ai.puzzle = copy.deepcopy(ai.clean_puzzle)           


class BreadthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.first_in_first_out(self.ai_tree.get_nodes_of_level(0)[0])
        self.puzzle = copy.deepcopy(self.saved_puzzle_move)        
        self.ai_tree = None
        
        return AI.move_find_path_of_state(self,winningstate,self.puzzle)
        
    def first_in_first_out(self,startNode):
        self.closedNodes = []
        self.openNodes = [startNode]
        
        self.clean_puzzle = copy.deepcopy(self.puzzle)
        winning_Node = startNode
        
        while len(self.openNodes) != 0:
            current = self.openNodes.pop(0)
            
            if self.puzzle.is_goal_match(current.state):
                return current            
            
            AI.backtracker(self,current)
            self.closedNodes.append(current)
            for nextnode in self.ai_tree.get_leaf_nodes(self.ai_tree.get_node_of_state(current.state)):
                if nextnode.get_height() > self.puzzle.get_max_level():
                    continue                
                if self.puzzle.node_compare(nextnode.state,self.closedNodes):
                    continue
                if self.puzzle.node_compare(nextnode.state,self.openNodes) == False:
                    self.openNodes.append(nextnode)
        return "Error"

class DepthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.last_in_last_out(self.ai_tree.get_nodes_of_level(0)[0])
        self.puzzle = copy.deepcopy(self.saved_puzzle_move)
        self.ai_tree = None
        
        return AI.move_find_path_of_state(self,winningstate,self.puzzle)
    
    def last_in_last_out(self,startNode): 
        self.closedNodes = []
        self.openNodes = [startNode]
        
        self.clean_puzzle = copy.deepcopy(self.puzzle)
        winning_Node = startNode
        
        while len(self.openNodes) != 0:
            current = self.openNodes.pop(0)
            
            if self.puzzle.is_goal_match(current.state):
                return current            
            AI.backtracker(self,current)
            
            self.closedNodes.append(current)
            temp_nodes = []
            for nextnode in self.ai_tree.get_leaf_nodes(self.ai_tree.get_node_of_state(current.state)):
                if nextnode.get_height() > self.puzzle.get_max_level():
                    continue
                if self.puzzle.node_compare(nextnode.state,self.closedNodes):
                    continue
                if self.puzzle.node_compare(nextnode.state,self.openNodes) == False:
                    temp_nodes.append(nextnode)
            
            merged_nodes = temp_nodes + self.openNodes
            self.openNodes = merged_nodes
        return "Error"
class AStarAI():
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.AStarSearch(self.ai_tree.get_nodes_of_level(0)[0])
        self.ai_tree = None
        self.puzzle = copy.deepcopy(self.saved_puzzle_move) 
        
        return  AI.move_find_path_of_state(self,winningstate,self.puzzle)
    def AStarSearch(self,startNode):
        heuristic_type = 2
        self.closedNodes = []
        self.openNodes = [startNode]
        self.heur = self.puzzle.heuristic(heuristic_type,startNode)
        self.g_score = dict()
        self.g_score.setdefault("default",["default",sys.maxsize])
        self.f_score = dict()
        self.f_score.setdefault("default",["default",sys.maxsize])
        self.g_score[startNode] = [startNode.state,0]
        self.f_score[startNode] = [startNode.state,self.heur]
        
        self.clean_puzzle = copy.deepcopy(self.puzzle)
        winning_Node = startNode
        while len(self.openNodes) != 0:
            current = self.get_state_with_lowest_f_score()
            
            if self.puzzle.is_goal_match(current.state):
                return current            
            
            AI.backtracker(self,current,heuristic_type)
            
            self.openNodes.remove(current)
            self.closedNodes.append(current)
            for nextnode in self.ai_tree.get_leaf_nodes(self.ai_tree.get_node_of_state(current.state)):
                exist = True
                if self.puzzle.node_compare(nextnode.state,self.closedNodes):
                    continue
                tentative_g_score = self.g_score[current][1] + self.puzzle.distance(current.state,nextnode.state)
                if self.puzzle.node_compare(nextnode.state,self.openNodes) == False:
                    self.openNodes.append(nextnode)
                    exist = False
                elif tentative_g_score >= self.find_g_score_equivalent(nextnode,self.g_score):
                    continue
                if exist:
                    actualnode = self.find_g_score_node(nextnode,self.g_score)
                else:
                    actualnode = nextnode
                self.g_score[actualnode] = [actualnode.state,tentative_g_score]
                self.f_score[actualnode] = [actualnode.state,self.g_score[actualnode][1] + self.heur]
            
            #AStarAI.print_states_nodes(self.openNodes)
            #AStarAI.print_states_nodes(self.closedNodes)            
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
            
            
        print("State: " + str(result_node.state) + " FScore: " + str(lowest_score) )
        return result_node
    def get_states(Nodes):
        lis = []
        for node in Nodes:
            lis.append(node.state)
        return lis
    def find_g_score_equivalent(self,node,g_score):
        for key in iter(g_score):
            if self.puzzle.proper_node(node.state) == self.puzzle.proper_node(g_score.get(key)[0]):
                return g_score.get(key)[1]
    def find_g_score_node(self,node,g_score):
        for key in iter(g_score):
            if self.puzzle.proper_node(node.state) == self.puzzle.proper_node(g_score.get(key)[0]):
                return key
            
    def print_states_nodes(nodes):
        strg = ""
        for node in nodes:
            strg += str(node.state) + "\n"
        print(strg + "\n")