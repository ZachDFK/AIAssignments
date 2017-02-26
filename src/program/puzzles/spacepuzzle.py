#space puzzle
from . import puzzle
import random
import copy
class SpacePuzzle(puzzle.Puzzle):
    
    def get_row(self):
        return self.row_len
    def get_column(self):
        return self.col_len
    
    def __init__(self,grid_dimension = '',aitype=0):
        self.init_grid(grid_dimension)
        self.number_of_moves = 0        
        self.init_state()
    
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
        
        self.init_win_grid()
        
    def init_win_grid(self):
        self.win_grid = []
        for num in range(0,self.total_num):
            self.number_array.append(num)
        for x in range(0,self.row_len):
            temp_row = []
            for y in range(self.col_len):
                if x+1 == self.row_len and y+1 == self.col_len :
                    temp_row.append(self.number_array.pop(0))
                else:
                    temp_row.append(self.number_array.pop(1))
            self.win_grid.append(temp_row)
        print(self.win_grid) 
    def get_random_value(self):
        max_value = len(self.number_array) -1 
        return self.number_array.pop(random.randint(0, max_value))
        
    def init_ai(self,aitype):
        pass
    def init_state(self):
        self.state = [self.check_out_of_place_values(),"default",0]
        self.init_state_tree()        
    def check_out_of_place_values(self):
        outofplace = 0
        for x in range(0,self.row_len):
            for y in range(0,self.col_len):
                if self.grid[x][y] != self.win_grid[x][y]:
                    outofplace += 1
        return outofplace
    def init_state_tree(self):
        self.possible_states = self.get_all_current_possible_states() # for the initial sate, all the possible states are at level 1
        self.state_tree = puzzle.StateTree(copy.deepcopy(self.state))
        self.update_state_tree(self.state_tree.baseroot)
  
    def update_state_tree(self,root,ai = 0):
        for state in self.possible_states:
            self.state_tree.add_node(puzzle.StateTreeNode(state),root)
        if ai == 0:
            print(self.state_tree)
    
    
    def get_moves(self):
        blank_cord = self.find_blank_spot()
        possible_moves = []
        if blank_cord[0] == 0:
            top,bot = [0,1]
        elif blank_cord[0] == self.row_len - 1:
            top,bot = [-1,0]
        else:
            top,bot = [-1,1]
            
        if blank_cord[1] == 0:
            left,right = [0,1]
        elif blank_cord[1] == self.col_len -1:
            left,right = [-1,0]
        else:
            left,right = [-1,1]
        
        cardinal = [top,bot,left,right]
        for index in range(0,len(cardinal)):
            top_bot = index - 2
            if top_bot < 0:
                temp = blank_cord[0] + cardinal[index]
                mod = 0
            else:
                temp = blank_cord[1] + cardinal[index]
                mod = 1
            if temp != blank_cord[mod]:
                if mod == 0:
                    move_str = str(temp) + "-" + str(blank_cord[1])
                else:
                    move_str = str(blank_cord[0]) + "-" + str(temp)
                possible_moves.append(move_str)
        return possible_moves
    
    def find_blank_spot(self):
        for x in range(0,self.row_len):
            for y in range(0,self.col_len):
                if self.grid[x][y] == 0:
                    return [x,y]
        return "Error"
    def get_all_current_possible_states(self,ai=0):
    
        current_puzz = copy.deepcopy(self)
        
        possible_states = []
        possible_moves = self.get_moves()
        for move in possible_moves:
            self = copy.deepcopy(current_puzz)            
            self.make_a_move(move,1)
            possible_states.append(self.state)
        self = copy.deepcopy(current_puzz)
        if ai == 0:
            print("Current state:" + str(self.state))
        
        return possible_states        
    
    def manual_move(self,choice):
        self.make_a_move(choice)
    def ai_move(self,step):
        pass
    def update_state(self,choice):
        self.state[0] = self.check_out_of_place_values()
        self.state[1] = choice
        self.state[2] = self.number_of_moves
    def is_goal_match(self,state = None):
        return state[0] == 0
    def heuristic(self,type,node= None ):
        pass
    def get_cost(self,state):
        pass
    def get_move_from_state(self,state):
        pass
    def make_a_move(self,choice,fake=0,ai=0):
        if choice == "default":
            print("Error!")
        cx,cy = choice.split("-")
        cx =int(cx)
        cy = int(cy)
        value = self.grid[cx][cy]
        
        for x in range(0,self.row_len):
            for y in range(0,self.col_len):
                curvalue = self.grid[x][y]
                if curvalue == 0:
                    curvalue = value
                elif curvalue == value:
                    curvalue = 0
                self.grid[x][y] = curvalue
            
        self.number_of_moves += 1       
        if fake  == 0:
            self.log_move(choice)
        self.update_state(choice)
        if fake == 0 or ai == 1:
            self.possible_states = self.get_all_current_possible_states(ai)
            self.update_state_tree(self.state_tree.get_node_of_state(self.state),ai)
    
    def log_move(self,choice):
        lstr = "Made a move at cordinate: "  + choice
        self.logofmoves.append(lstr)
        print(lstr)
    