#Puzlle gui

from appJar import gui
from .. import pseudomain
from ..definitions.constants import GuiConstants
from ..puzzles import transpuzzle,spacepuzzle


class PuzzleGUI:
   
   
    def selectedbox(self,chck):
        print(chck)
        
        
    def move(self,btn):
        self.puzapp.get
        
    def press(self,btn):
        if btn == GuiConstants._GuiConstants__backtomain:
            self.cancel()
        
        elif btn == "Show bridge":
            self.trans()
        else:
            self.space()
    
    
    def __init__(self,type):
        self.puzapp = gui(type,GuiConstants._GuiConstants__puzzle_size)
        self.puzapp.addButton(GuiConstants._GuiConstants__backtomain, self.press, 0, 0,colspan=4)
        self.pre_puzzle_set_up(type)
        self.puzapp.setImageLocation("program/definitions/images/")                
        self.puzapp.go()
    
    def get_puzzle(self,type,option):
        if type == GuiConstants._GuiConstants__transpuzname:
            self.puzzle = transpuzzle.TransportPuzzle(option)
        else:
            self.puzzle = spacepuzzle.SpacePuzzle(option)
    
    def pre_puzzle_set_up(self,type):
        self.puzapp.startLabelFrame("Puzzle",1,0)
        if type ==  GuiConstants._GuiConstants__spacepuzname:
            self.puzapp.addLabel("tempText", text="Not yet completed", 
                                 row=0, 
                                 column=0,
                                 colspan=0,
                                 rowspan=0)
        else:
            self.puzapp.addLabel("adventurerSelect", text="Choose the number of adventurers(Leave blank for default):", row=0, column=0)
            self.puzapp.addEntry("numAdventurer", row=0, column=2)
            self.puzapp.addButton("Show bridge", self.press,row=0,column=3)
            
        self.puzapp.stopLabelFrame()
    
    def cancel(self):
        self.puzapp.stop()
    
    def trans(self):
        self.puzapp.startLabelFrame("Bridge",2,0)
        activepuzzle = transpuzzle.TransportPuzzle(self.puzapp.getEntry("numAdventurer"))
        self.puzapp.startLabelFrame("Adventurers",0,0)
        self.puzapp.addLabel("allAdventurers", text="Your adventurers:", row=0, column=0)
        
        for num in range(0,len(activepuzzle.start_adventurers)):
            self.puzapp.addCheckBox(activepuzzle.start_adventurers[num].print_adventurer(), row=1,column=num,colspan=0)
            self.puzapp.setCheckBoxFunction(activepuzzle.start_adventurers[num].print_adventurer(),self.selectedbox)
        self.puzapp.stopLabelFrame()
        
        self.puzapp.addLabel("leftAdvent", text=activepuzzle.get_start_string(), row=1, column=0, colspan=0, 
                            rowspan=0)
        # self.puzapp.addImage("bridge","bridge.gif",1,1)
        self.puzapp.addLabel("bridge", text=">======<", row=1, column=1,colspan=0)
        self.puzapp.addLabel("rightAdvent", text=activepuzzle.get_end_string(), row=1, column=2,colspan=0)
        self.puzapp.addButton("Move Selected", self.move, row=2)
       
        self.puzapp.stopLabelFrame()
        
    
    def space(self):
        print("I'm in space")

    #self.puzapp.addLabel("selectionText", "Choose 2 adventurers:", 
                                 #row=0, 
                                 #column=0, 
                                 #colspan=0, 
                                 #rowspan=0)
    #self.puzapp.addLabelOptionBox("selectionBox", , row=0, column=1, 
                                          #colspan=2)

                                          