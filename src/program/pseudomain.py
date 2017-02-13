from appJar import gui
from .definitions.constants import GuiConstants
from .puzzles import puzzlegui

class Main:
    
    def press(self,btn):
        if btn == GuiConstants._GuiConstants__quit:
            self.app.stop()
        
        else:
            print("Starting " + btn + " ... ")
       
        
            puzzleapp = puzzlegui.PuzzleGUI(btn)
            
            
    def __init__(self):
        self.app = gui(GuiConstants._GuiConstants__progtitle,GuiConstants._GuiConstants__menu_size)
        self.app.addLabel(GuiConstants._GuiConstants__title,GuiConstants._GuiConstants__welcome, 0, 0)
        self.app.addLabel("authorFiller","Name:\tZacharie Gauthier \nStudent ID:\t100897337",1,0)
        self.app.addButtons([GuiConstants._GuiConstants__transpuzname,GuiConstants._GuiConstants__spacepuzname,GuiConstants._GuiConstants__quit],self.press,3,0,2)
        self.app.go()
        
    


