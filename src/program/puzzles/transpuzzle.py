#Comodity transportation puzzle

from . import puzzle
import random
import copy
from ..ai import ai
 
 
class TransportPuzzle(puzzle.Puzzle):
    
    
    
    
    def __init__(self,numb = 0,aitype=0):
        
        self.start_adventurers = self.generate_start_adventurers(numb) 
        self.end_adventurers = self.generate_end_adventurers()
        self.init_state()
        self.init_ai(aitype)
        
    def init_ai(self,aitype):
        if aitype == 0:
            self.ai = Ai()
    def init_state(self):
        self.level = 0
        self.selectedmoves = []
        self.state = [len(self.start_adventurers),len(self.end_adventurers),0,0,"0-0"]
        print(self.state)
        self.init_state_tree()
    def init_state_tree(self):
        self.possible_states = self.get_all_current_possible_states(self.level) # for the initial sate, all the possible states are at level 1
        self.state_tree = puzzle.StateTree(copy.deepcopy(self.state))
        self.update_state_tree(self.state_tree.baseroot)
            
    def update_state_tree(self,root):
        for state in self.possible_states:
            self.state_tree.add_node(puzzle.StateTreeNode(state),root)
        print(self.state_tree)    
    
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
    def get_all_current_possible_states(self,level):
        order = level%2
        current_puzz = copy.deepcopy(self)
        
        possible_states = []
        possible_moves = self.get_moves(order)
        for move in possible_moves:
            self = copy.deepcopy(current_puzz)            
            self.make_a_move(move,1)
            possible_states.append(self.state)
        self = copy.deepcopy(current_puzz)
        print("Current state:" + str(self.state))
        
        return possible_states
    def generate_start_adventurers(self,numb):
        
        if numb == '':
            adventurers = self.gen_numb_zero_start()
        else:
            try:
                numb = int(numb)            
            except ValueError:
                print("Needs a number value please!")
                
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
    def update_state(self,order,time,choice):
        self.state[0] = len(self.start_adventurers)
        self.state[1] = len(self.end_adventurers)
        self.state[2] = order
        self.state[3] += time
        self.state[4] = choice
    def is_goal_match(self):
        answer = False
        if self.state[0] == 0 and self.state[2] == 1:
            answer = True
        return answer

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
    
    def make_a_move(self,choice,fake=0):
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
        elif order ==1 and len(advchoice) == 1:
            adventurer1 = self.get_adventurer(advchoice[0],order)      
            self.end_adventurers.remove(adventurer1)
            self.start_adventurers.append(adventurer1)
            order = 0
        else:
            print("Illegal move")
            return 0
        if fake == 0:
            self.level += 1
            print("Total moves made: " + str(self.level))
        
        time = TransportPuzzle.find_choice_time(adventurer1,adventurer2)
        
        self.update_state(order,time,choice)
        if fake == 0:
            self.possible_states = self.get_all_current_possible_states(self.level)
            self.update_state_tree(self.state_tree.get_node_of_state(self.state))
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
        if len(advarr) >= 1:
            return advarr
    
    
    
    def merge(righarr,leftarr):
        