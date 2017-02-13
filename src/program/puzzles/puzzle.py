#puzzle Class

from abc import ABC, abstractmethod
class Puzzle():
    
    movestates = []
    logofmoves = []

    
    @abstractmethod
    def find_states():
        pass
    
    @abstractmethod 
    def is_over():
        pass
    
    @abstractmethod
    def make_a_move():
        pass
    @abstractmethod
    def is_goal_match(state):
        pass
    def log_move(state):
        pass
    
    def print_move(state):
        pass
    
    def get_moves():
        return movestates