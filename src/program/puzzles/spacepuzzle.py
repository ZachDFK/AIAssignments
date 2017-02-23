#space puzzle
from . import puzzle
import random
class SpacePuzzle(puzzle.Puzzle):
    
    def get_row(self):
        return self.row_len
    def get_column(self):
        return self.col_len
    
    def __init__(self,grid_dimension = '',aitype=0):
        self.init_grid(grid_dimension)
     
    
    def init_grid(self,grid_dimension):
 
        if grid_dimension == '':
            self.row_len = 3
            self.col_len = 3
        else:
            self.row_len, self.col_len = grid_dimension.split("-")
            self.row_len = int(self.row_len)
            self.col_len = int(self.col_len)
        self.total_num = self.row_len * self.col_len
        self.number_array = []
        self.grid = []
        
        
        for num in range(0,self.total_num):
            self.number_array.append(num)
        for x in range(self.row_len):
            temp_row = []
            for y in range(self.col_len):
                temp_row.append(self.get_random_value())
            self.grid.append(temp_row)
        
                
    def get_random_value(self):
        max_value = len(self.number_array) -1 
        return self.number_array.pop(random.randint(0, max_value))
        
    def init_ai(self,aitype):
        pass
    def init_state(self):
        pass
    def init_state_tree(self):
        pass
    def update_state_tree(self,root,ai = 0):
        pass    
    
    
    def get_moves(self,order):
        pass
    def get_all_current_possible_states(self,level,ai=0):
        pass
    def generate_start_adventurers(self,numb):
        pass
    def manual_move(self):
        pass
    def ai_move(self,step):
        pass
    def gen_numb_any_start(self,numb):
        pass
    def gen_numb_zero_start(self):
        pass
    def generate_end_adventurers(self):
        pass
    def get_adventurer(self,name,order):
        pass
    def update_state(self,order,time,choice):
        pass
    def is_goal_match(self,state = None):
        pass
    def heuristic(self,type,node= None ):
        pass
    
    def distance(self,state1,state2):
        pass
    def get_start_adventurers_total_moves(self):
        pass
    def get_cost(self,state):
        pass
    def get_start_string(self):
        pass
    def get_end_string(self):
        pass
    def get_advent_string(self,side):
        pass
    def get_move_from_state(self,state):
        pass
    def make_a_move(self,choice,fake=0,ai=0):
        pass
    def log_move(self,advchoice,order,time):
        pass
    def find_choice_time(adventurer1,adventurer2):
        pass