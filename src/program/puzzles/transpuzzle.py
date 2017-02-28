#Comodity transportation puzzle

from . import puzzle
import random
import copy
from ..ai import ai
 
 
class TransportPuzzle(puzzle.Puzzle):
    
    
    
    
    def __init__(self,numb = '',aitype=0):
        
        self.start_adventurers = self.generate_start_adventurers(numb) 
        self.end_adventurers = self.generate_end_adventurers()
        self.total_time = 0
        
        self.init_state()
        self.init_ai(aitype)
        
    def init_ai(self,aitype):
        self.ai = ai.AI(self,aitype)
        self.listofmoves = []
    def init_state(self):
        self.level = 0
        self.selectedmoves = []
        self.state = [len(self.start_adventurers),len(self.end_adventurers),0,"default",[self.get_start_string(),self.get_end_string()]]
        print(self.state)
        self.init_state_tree()
    def init_state_tree(self):
        self.possible_states = self.get_all_current_possible_states(self.level) # for the initial sate, all the possible states are at level 1
        self.state_tree = puzzle.StateTree(copy.deepcopy(self.state))
        self.update_state_tree(self.state_tree.baseroot)
            
    def update_state_tree(self,root,ai = 0):
        for state in self.possible_states:
            self.state_tree.add_node(puzzle.StateTreeNode(state),root)
        #if ai == 0:
            #print(self.state_tree)    
    
    def get_moves(self,order):
        moves =[]
        if order == 0:
            move_arrar = copy.deepcopy(self.start_adventurers)
        else:
            move_arrar = copy.deepcopy(self.end_adventurers)
        while len(move_arrar) > 0:
            if order == 1:
                moves.append(move_arrar.pop(0).get_name())
            else:
                adv1 = move_arrar.pop(0).get_name()
                adv2arr = copy.deepcopy(move_arrar) 
                while len(adv2arr) >0:
                    moves.append( adv1 + "-" + adv2arr.pop(0).get_name())
        return moves
    def get_all_current_possible_states(self,level,ai=0):
        order = level%2
        current_puzz = copy.deepcopy(self)
        
        possible_states = []
        possible_moves = self.get_moves(order)
        for move in possible_moves:
            self = copy.deepcopy(current_puzz)            
            self.make_a_move(move,1)
            possible_states.append(self.state)
        self = copy.deepcopy(current_puzz)
        #if ai == 0:
            #print("Current state:" + str(self.state))
        
        return possible_states
    def generate_start_adventurers(self,numb):
        
        if numb == '':
            self.max_level = 9
            adventurers = self.gen_numb_zero_start()
        else:
            
            try:
                numb = int(numb)            
            except ValueError:
                print("Needs a number value please!")
            
            self.max_level = numb*2 -3                 
            adventurers = self.gen_numb_any_start(numb)
        
        return adventurers
            
    def manual_move(self):
        if len(self.selectedmoves) > 1:
            adv1,time1 = self.selectedmoves[0].split(": ")
            adv2,time2 = self.selectedmoves[1].split(": ")
            if( time1 <= time2):
                move = adv1 + "-" + adv2
            else:
                move = adv2 + "-" + adv1
        elif self.selectedmoves != None: 
            move = self.selectedmoves[0].split(": ")[0]
        else:
            print("Illegal Move")
        self.make_a_move(move)
        self.selectedmoves.clear()
    
    def ai_move(self,step):
        if self.listofmoves == []:
            self.listofmoves = self.ai.real_ai.find_list_of_moves()
            
        while len(self.listofmoves) >0:
            self.make_a_move(self.listofmoves.pop(0))
            if(step == 1):
                break
        
        
        
    def gen_numb_any_start(self,numb):
        adventurers = []
        
        for num in range(0,numb):
            if num == 0:
                walktime = random.randint(1,3)
            else:
                walktime = adventurers[num-1].get_walktime() + random.randint(1,3)
            adventurers.append(Adventurer("P"+ str(num+1),walktime))
        return adventurers
        
    
    def gen_numb_zero_start(self):
        adventurers = []
        for num in range(0,6):
            if num == 0:
                walktime = 1
            elif num ==1:
                walktime = adventurers[num-1].get_walktime() + 1
            else:
                walktime = adventurers[num-1].get_walktime() + adventurers[num-2].get_walktime()
            
            adventurers.append(Adventurer("P" + str(num+1), walktime))
        return adventurers
   
    def generate_end_adventurers(self):
        return  []
    def get_adventurer(self,name,order):
        if order == 0:
            modified_array = self.start_adventurers
        else:
            modified_array = self.end_adventurers
        for index in range(0,len(modified_array)):
            if modified_array[index].get_name() == name:
                return modified_array[index]
        return Adventurer("Error",0)    
    def update_state(self,order,choice):
        self.state[0] = len(self.start_adventurers)
        self.state[1] = len(self.end_adventurers)
        self.state[2] = order
        self.state[3] = choice
        self.state[4] = self.map_board()
        
    def is_goal_match(self,state = None):
        if state == None:
            state = self.state
        answer = False
        
        if state[0] == 0 and state[2] == 1:
            answer = True
        return answer
    def heuristic(self,type,node= None ):
        
        type_0 = self.get_start_adventurers_total_moves()
        
        add = 0
        if len(self.end_adventurers) >0:
            add = self.end_adventurers[0].get_walktime()
        type_1= self.get_start_adventurers_total_moves() + add
        
        if type == 0:
            return type_0
        elif type == 1:
            return type_1
        else:
            return (type_0 + type_1)/2
            
    
    def distance(self,state1,state2):
        return abs(self.get_cost(state1) - self.get_cost(state2))
    

    def proper_node(self,state=None):
        if state == None:
            state = self.state
        return [self.get_board(state),self.get_order(state)]
    
    def node_compare(self,state,nodes):
        for node in nodes:
            if self.get_board(state) ==  self.get_board(node.state) and self.get_order(state) == self.get_order(node.state):
                return True
        return False    
    
    def get_order(self,state= None):
        if state == None:
            state = self.state
        return state[2]
    def get_start_adventurers_total_moves(self):
        total = 0
        for adv in self.start_adventurers:
            total =+ adv.get_walktime()
        return total
    def get_cost(self,state=None):
        if self.get_move_from_state(state) == "default":
            return 0
        advchoice = self.get_move_from_state(state).split("-")
        adventurer1 = None
        adventurer2 = None
        if len(advchoice) > 1:
            adventurer1 = self.get_adventurer(advchoice[0],0)
            adventurer2 = self.get_adventurer(advchoice[1],0)             
        else:
            adventurer1 = self.get_adventurer(advchoice[0],1)
            
        return TransportPuzzle.find_choice_time(adventurer1,adventurer2)
    
    def get_final_cost(self):
        return self.total_time
    
    def get_start_string(self):
        return self.get_advent_string("left")
    def get_end_string(self):
        return self.get_advent_string("right")
    
    def get_advent_string(self,side):
        adventarray = self.end_adventurers
        if side == "left":
            adventarray = self.start_adventurers
        
        retstr = "["
        for adv in adventarray:
            retstr += adv.get_name() + ","
        retstr += "]"
        return retstr
    def get_move_from_state(self,state):
        return state[3]
        
    def make_a_move(self,choice,fake=0,ai=0):
        advchoice = choice.split('-')        
        adventurer1 = None
        adventurer2 = None
        order = self.state[2]
        if order == 0  and len(advchoice) == 2:
            adventurer1 = self.get_adventurer(advchoice[0],order)
            adventurer2 = self.get_adventurer(advchoice[1],order)
            self.start_adventurers.remove(adventurer1)
            self.start_adventurers.remove(adventurer2)
            self.end_adventurers.append(adventurer1)
            self.end_adventurers.append(adventurer2)    
            order = 1       
        elif order == 1 and len(advchoice) == 1:
            adventurer1 = self.get_adventurer(advchoice[0],order)      
            self.end_adventurers.remove(adventurer1)
            self.start_adventurers.append(adventurer1)
            order = 0
        else:
            if ai == 0:
                print("Illegal move")
            return 0
        self.start_adventurers = Adventurer.sort_adventurer_list(self.start_adventurers)
        self.end_adventurers = Adventurer.sort_adventurer_list(self.end_adventurers)
        
        if fake == 0 or ai == 1:
            self.level += 1
            if ai == 0:
                print("Total moves made: " + str(self.level))
        
        time = TransportPuzzle.find_choice_time(adventurer1,adventurer2)
        self.total_time += time
        self.update_state(order,choice)
        if fake == 0 or ai == 1:
            self.possible_states = self.get_all_current_possible_states(self.level,ai)
            self.update_state_tree(self.state_tree.get_node_of_state(self.state),ai)
        if fake == 0:
            self.log_move(advchoice,order,time)
        
    def log_move(self,advchoice,order,time):
        if order == 1:
            torchloc = " right"
            other = advchoice[1] = " and " + advchoice[1]
        else:
            torchloc = " left"
            other = ""
        choicestr = advchoice[0] +  other + " took " +  str(time) + " minutes to cross the bridge. The torch is on the " + torchloc  + " side."
        self.logofmoves.append(choicestr)
        print("Current State:" + str(self.state))
        puzzle.Puzzle.print_move(choicestr)

    def find_choice_time(adventurer1,adventurer2):
        time = adventurer1.get_walktime()
        if adventurer2 != None:
            time = max(adventurer1.get_walktime(),adventurer2.get_walktime())
        return time
    
    def get_board(self,state=None):
        if state == None:
            state = self.state
        return state[4]
    
    def map_board(self):
        return [self.get_start_string(),self.get_end_string()]
    
    def get_max_level(self):
        return self.max_level
class Adventurer:
    
    def __init__(self,name,walktime):
        self.name = name
        self.walktime = walktime
        
    def get_name(self):
        return self.name
    def get_walktime(self):
        return self.walktime
    def print_adventurer(self):
        return self.get_name() + ": " + str(self.get_walktime())
    
    def sort_adventurer_list(advarr):
        if len(advarr) <= 1:
            return advarr
        left = []
        right = []
        for index in range(0,len(advarr)):
            if index < len(advarr)/2:
                left.append(advarr[index])
            else:
                right.append(advarr[index])
        
        left = Adventurer.sort_adventurer_list(left)
        right = Adventurer.sort_adventurer_list(right)
        
        return Adventurer.merge(left,right)
    
    def merge(leftarr,rightarr):
        result = []
        while len(leftarr) > 0 and len(rightarr) > 0:
            if leftarr[0].get_walktime() <= rightarr[0].get_walktime():
                result.append(leftarr.pop(0))
            else:
                result.append(rightarr.pop(0))
        
        while  len(leftarr) > 0:
            result.append(leftarr.pop(0))
        while len(rightarr) > 0:
            result.append(rightarr.pop(0))
        return result