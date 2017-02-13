#Comodity transportation puzzle

from . import puzzle
import random
 
 
class TransportPuzzle(puzzle.Puzzle):
    
    
    def __init__(self,numb = 0):
        self.start_adventurers = self.generate_start_adventurers(numb) 
        self.end_adventurers = self.generate_end_adventurers()
    
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
            
    
    def gen_numb_any_start(self,numb):
        adventurers = []
        
        for num in range(0,numb):
            if num == 0:
                walktime = random.randint(1,3)
            else:
                walktime = adventurers[num-1].get_walktime() + random.randint(1,3)
            adventurers.append(Adventurer("Adventure_"+ (num+1),walktime))
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
    
    
    def get_start_string(self):
        return self.get_advent_string("left")
    def get_end_string(self):
        return self.get_advent_string("right")
    
    def get_advent_string(self,side):
        adventarray = self.end_adventurers
        if side == "left":
            adventarray = self.start_adventurers
        retstr = "["
        for num in range(0, len(adventarray)):
            retstr += adventarray[num].get_name() + ","
        retstr += "]"
        return retstr
    
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