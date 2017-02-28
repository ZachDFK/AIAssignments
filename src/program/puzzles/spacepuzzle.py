#space puzzle
from . import puzzle
import random
import copy
from ..ai import ai
class SpacePuzzle(puzzle.Puzzle):
    
    def get_row(self):
        return self.row_len
    def get_column(self):
        return self.col_len
    
    def __init__(self,grid_dimension = '',aitype=0):
        self.number_of_moves = 0              
        self.init_grid(grid_dimension)  
        self.init_state()
        self.init_ai(aitype)
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
        self.init_win_grid()
        self.state= [0,"init",[0]]
        self.grid = copy.deepcopy(self.win_grid)
        
        
        self.max_level = self.total_num*self.total_num
        for num in range(0,self.max_level):
            pos_moves = self.get_moves()
            self.make_a_move(pos_moves[random.randint(0,len(pos_moves)-1)],1)
        
        self.number_of_moves = 0
        
        
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
        self.ai = ai.AI(self,aitype)
        self.listofmoves = []        
        
    def init_state(self):
        self.state = [self.check_out_of_place_values(),"default",self.grid]
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
        #if ai == 0:
            #print(self.state_tree)
    
    
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
        
        if choice in self.get_moves():
            self.make_a_move(choice)
        else:
            print("Move unavailable")
    def ai_move(self,step):
        if self.listofmoves == []:
            self.listofmoves = self.ai.real_ai.find_list_of_moves()
            
        while len(self.listofmoves) >0:
            self.make_a_move(self.listofmoves.pop(0))
            if(step == 1):
                break
    def update_state(self,choice):
        self.state[0] = self.check_out_of_place_values()
        self.state[1] = choice
        self.state[2] = self.grid
    def is_goal_match(self,state = None):
        if state == None:
            state = self.state
        return state[0] == 0
    def heuristic(self,type,node= None ):
        type_0 = self.get_cost(node.state)
        type_1 = self.get_manhattan()
        if type == 0:
            return type_0
        elif type == 1:
            return type_1
        else:
            return (type_0 + type_1)/2
    
    def get_cost(self,state= None):
        if state == None:
            state = self.state
        return state[0]
    
    def get_final_cost(self,state= None):
        return self.number_of_moves
    def get_move_from_state(self,state):
        if state == None:
            state = self.state
        return state[1]
    def make_a_move(self,choice,fake=0,ai=0):
        if choice == "default":
            print("Illegal Move")
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
    def distance(self,state1,state2):
        
        return 1
    
    def get_board(self,state=None):
        if state == None:
            state = self.state
        return state[2]        
    
    def proper_node(self,state=None):
        if state == None:
            state = self.state
        return self.get_board(state)
    def node_compare(self,state,nodes):
        for node in nodes:
            if self.get_board(state) ==  self.get_board(node.state):
                return True
        return False
    
    def get_manhattan(self):
        number_position = []
        winner_position = []
        manhattan_number = 0
        for x in range(0,self.row_len):
            for y in range(0,self.col_len):
                number_position.append([self.grid[x][y],x,y])
                winner_position.append([self.win_grid[x][y],x,y])
        for numw in range(0,len(winner_position)):
            for num in range(0,len(number_position)):
                if number_position[num][0] == winner_position[numw][0]:
                    absx = abs(number_position[num][1] - winner_position[numw][1])
                    absy = abs(number_position[num][2] - winner_position[numw][2])
                    manhattan_number += absx + absy
        return manhattan_number
    
    def get_max_level(self):
        return self.max_level