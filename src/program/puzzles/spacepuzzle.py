#space puzzle
from . import puzzle
class SpacePuzzle(puzzle.Puzzle):
    
    
    
    def __init__(self,boardsize):
        self.board = self.generate_board(boardsize)
        
    
    
    
    def generate_baord(boardsize):
        row,col = boardsize.split('x')
        print("Size of board is \nRow: " + row + " \nCol:" + col)