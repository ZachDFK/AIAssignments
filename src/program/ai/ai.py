#AI class
import copy
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

    def find_path_of_winning_state(sai,state):
        listofmoves = []
        
        while state != self.puzzle.state:
            listofmoves.insert(0,self.puzzle.get_move_from_state(state))
            state = sai.ai_tree.get_node_of_state(state).root
        return listofmoves
        
        
class BreadthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
        self.saved_puzzle_move = copy.deepcopy(self.puzzle)
        
    
        self.ai_tree = copy.deepcopy(self.puzzle.state_tree)        
        winningstate = self.first_in_first_out(0)
        self.puzzle = copy.deepcopy(self.saved_puzzle_move)        
        return AI.find_path_of_winning_state(self,winningstate)
        
    def first_in_first_out(self,level):
        print(self.ai_tree)
        if self.puzzle.is_goal_match():
            return self.state
        else:
            clean_puzzle = copy.deepcopy(self.puzzle)
            level +=1
            for node in self.ai_tree.get_nodes_of_level(level):
                temp_move = self.puzzle.get_move_from_state(node.state)
                self.puzzle.make_a_move(temp_move,1,1)
                if self.puzzle.is_goal_match():
                    return self.state      
                
                for c_node in self.puzzle.state_tree.get_leaf_nodes(self.puzzle.state_tree.get_node_of_state(self.puzzle.state)):
                    self.ai_tree.add_node(c_node,node)
                
                self.puzzle = copy.deepcopy(clean_puzzle)
            return self.first_in_first_out(level)
class DepthFirstAI():
    
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_moves(self):
            pass    

class AStarAI():
    def __init__(self,puzzle):
        self.puzzle = puzzle
    def find_list_of_move(self):
            pass    
