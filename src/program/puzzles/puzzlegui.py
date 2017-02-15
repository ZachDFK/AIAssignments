#Puzlle gui

import appJar
from .. import pseudomain
from ..definitions.constants import GuiConstants
from ..puzzles import transpuzzle,spacepuzzle


class PuzzleGUI:
   
   
    def selectedbox(self,chck):
        print(chck)
        
        if self.puzapp.getCheckBox(chck) == False:
            removedchck = self.activepuzzle.selectedmoves.remove(chck)            
        else:
            if len(self.activepuzzle.selectedmoves) > 1 or (len(self.activepuzzle.selectedmoves) >0 and self.activepuzzle.state[2] ==1) :
                removedchck = self.activepuzzle.selectedmoves.pop(0)
                self.puzapp.setCheckBox(removedchck,False)
            self.activepuzzle.selectedmoves.append(chck)
            
    def move(self,btn):
        if btn == "Move Selected":
            self.activepuzzle.manual_move()
        elif btn == "Run AI Step":
            sefl.activepuzzle.ai_move(True)
        else:
            self.activepuzzle.ai_move(False)
        
        self.update_bridge()
        
    def press(self,btn):
        if btn == GuiConstants._GuiConstants__backtomain:
            self.cancel()
        
        elif btn == "Show bridge":
            self.trans()
        else:
            self.space()
    
    
    def __init__(self,type):
        self.puzapp = appJar.gui(type,GuiConstants._GuiConstants__puzzle_size)
        #self.puzapp.addButton(GuiConstants._GuiConstants__backtomain, self.press, 0, 0,colspan=4)
        self.pre_puzzle_set_up(type)
        self.puzapp.setImageLocation("program/definitions/images/")                
        self.puzapp.go()
    
    def get_puzzle(self,type,option):
        if type == GuiConstants._GuiConstants__transpuzname:
            self.puzzle = transpuzzle.TransportPuzzle(option)
        else:
            self.puzzle = spacepuzzle.SpacePuzzle(option)
    
    def pre_puzzle_set_up(self,type):
        self.puzapp.addRadioButton("aitype", "Breadth First",1,0,1)
        self.puzapp.addRadioButton("aitype","Depth First",1,1,1)
        self.puzapp.addRadioButton("aitype","A*",1,2,1)
        
        if type ==  GuiConstants._GuiConstants__spacepuzname:
            self.puzapp.addLabel("sizeOfGrid", text="Size of Grid:", 
                                 row=0, 
                                 column=0,
                                 colspan=0,
                                 rowspan=0)
            self.puzapp.addEntry("x-y",row=0,column=2)
        else:
            self.puzapp.addLabel("adventurerSelect", text="Choose the number of adventurers(Leave blank for default):", row=0, column=0)
            self.puzapp.addEntry("numAdventurer", row=0, column=2)
            self.activepuzzle = transpuzzle.TransportPuzzle(self.puzapp.getEntry("numAdventurer"),self.puzapp.getRadioButton("aitype"))            
            self.puzapp.addButton("Show bridge", self.press,row=0,column=3)
            
            
    
    def cancel(self):
        self.puzapp.stop()
    
    def trans(self):
        self.puzapp.addLabel("allAdventurers", text="Available adventurers:", row=3, column=0)
        if self.activepuzzle.state[2] == 0 :
            advarr = self.activepuzzle.start_adventurers
        else:
            advarr = self.activepuzzle.end_adventurers
    
        for num in range(0,len(advarr)):
            self.puzapp.addCheckBox(advarr[num].print_adventurer(), row=3,column=num+1,colspan=0)
            self.puzapp.setCheckBoxFunction(advarr[num].print_adventurer(),self.selectedbox)
        
        
        self.puzapp.addLabel("leftAdvent", text=self.activepuzzle.get_start_string(), row=5, column=0, colspan=0, 
                            rowspan=0)
        # self.puzapp.addImage("bridge","bridge.gif",1,1)
        self.puzapp.addLabel("bridge", text=">======<", row=5, column=1,colspan=0)
        self.puzapp.addLabel("rightAdvent", text=self.activepuzzle.get_end_string(), row=5, column=2,colspan=0)
        self.puzapp.addButtons(["Move Selected","Run AI Step","Run AI Full"], self.move, row=6)
        
    def update_bridge(self):
        if self.activepuzzle.state[2] == 0 :
            advarr = self.activepuzzle.start_adventurers
            inadv  = self.activepuzzle.end_adventurers
        else:
            advarr = self.activepuzzle.end_adventurers
            inadv  = self.activepuzzle.start_adventurers

        for num in range(0,len(inadv)):
            self.puzapp.removeCheckBox(inadv[num].print_adventurer())
        
        for num in range(0,len(advarr)):
            # I know this is a horrable hack of job
            try:
                self.puzapp.addCheckBox(advarr[num].print_adventurer(), row=3,column=num+1,colspan=0)
            except(appJar.appjar.ItemLookupError):
                print("Error")
                self.puzapp.setCheckBox(advarr[num].print_adventurer(), ticked=False)
            self.puzapp.setCheckBoxFunction(advarr[num].print_adventurer(),self.selectedbox)
            
        self.puzapp.setLabel("leftAdvent", text=self.activepuzzle.get_start_string())
        self.puzapp.setLabel("rightAdvent", text=self.activepuzzle.get_end_string())
        if self.activepuzzle.is_goal_match():
            print("Won in :" + str(self.activepuzzle.state[3]) + " minutes!")
            self.puzapp.removeButton("Move Selected")
            self.puzapp.warningBox("winLabel","Won in :" + str(self.activepuzzle.state[3]) + " minutes!")
            self.puzapp.setLabelFunction("winLabel",self.stop())
    
    def space(self):
        print("I'm in space")


                                          