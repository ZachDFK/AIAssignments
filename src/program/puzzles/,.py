#Puzlle gui

from appJar import gui
from .. import pseudomain
from ..definitions.constants import GuiConstants
from ..puzzles import transpuzzle,spacepuzzle


class PuzzleGUI:
   
   
   
   
    def press(self,btn):
        if btn == GuiConstants._GuiConstants__backtomain:
            self.cancel()
        
        elif btn == "Show bridge":
            self.trans()
        else:
            self.space()
    
    
    def __init__(self,type):
        self.puzapp = gui(type,GuiConstants._GuiConstants__size)
        self.puzapp.addButton(GuiConstants._GuiConstants__backtomain, self.press, 0, 0,colspan=4)
        self.build_body(type)
        
        self.puzapp.go()
    
    
    def get_puzzle(self,type,option):
        if type == GuiConstants._GuiConstants__transpuzname:
            self.puzzle = transpuzzle.TransportPuzzle(option)
        else:
            self.puzzle = spacepuzzle.SpacePuzzle(option)
    
    def build_body(self,type):
        self.puzapp.startLabelFrame("Puzzle",0,0)
        if type ==  GuiConstants._GuiConstants__spacepuzname:
            self.puzapp.addLabel("tempText", text="Not yet completed", 
                                 row=0, 
                                 column=0,
                                 colspan=0,
                                 rowspan=0)
        else:
            self.puzapp.addLabel("adventurerSelect", text="Choose the number of adventurers(Leave blank for default):", row=0, column=0)
            self.puzapp.addEntry("numAdventurer", row=0, column=2)
            self.puzapp.addButton("Show bridge", self.press,row=0,column=0)
            
        self.puzapp.stopLabelFrame()
    
    def cancel(self):
        self.puzapp.stop()
    def trans(self):
        self.puzapp.startLabelFrame("bridge",)
    def space(self):
        print("I'm in space")

    #self.puzapp.addLabel("selectionText", "Choose 2 adventurers:", 
                                 #row=0, 
                                 #column=0, 
                                 #colspan=0, 
                                 #rowspan=0)
    #self.puzapp.addLabelOptionBox("selectionBox", , row=0, column=1, 
                                          #colspan=2)

                                          