'''Farmer_Fox.py
[STUDENTS: REPLACE THE FOLLOWING INFORMATION WITH YOUR
OWN:]
by Yining Wei and Hiba Abbas
UWNetIDs: yininw3, hibaa3
Student numbers: 2375867, 2222373

Assignment 2, in CSE 415, Winter 2025
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

# Put your metadata here, in the same format as in HumansRobotsFerry.
# <METADATA>


PROBLEM_NAME = "Farmer_Fox"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Y. Wei', 'H. Abbas']
PROBLEM_CREATION_DATE = "21-Jan-2025"
PROBLEM_DESC = \
    '''This formulation of Farmer, Fox, Chichen, and Grain problem uses generic
Python 3 constructs and has been tested with Python 3.9
'''
# </METADATA>

#<COMMON_DATA>
Farmer_on_left = 1
Fox_on_left = 1
Chicken_on_left = 1
Grain_on_left = 1
LEFT = 0
RIGHT = 1

# Start your Common Code section here.

class State:
    def __init__(self, old = None):
        if old is None:
            #Init everything to the left
            self.farmer_on_left = 1
            self.fox_on_left = 1
            self.chicken_on_left = 1
            self.grain_on_left = 1
            self.boat = LEFT
        else:
            #Init everything to the old
            self.farmer_on_left = old.farmer_on_left
            self.fox_on_left = old.fox_on_left
            self.chicken_on_left = old.chicken_on_left
            self.grain_on_left = old.grain_on_left
            self.boat = old.boat
    
    def __eq__(self,s2):
        #If not in the same position, return False
        if self.boat != s2.boat: return False
        if self.farmer_on_left != s2.farmer_on_left: return False
        if self.fox_on_left != s2.fox_on_left: return False
        if self.chicken_on_left != s2.chicken_on_left: return False
        if self.grain_on_left != s2.grain_on_left: return False
        return True
    
    def __str__(self):
        txt = "\n Boat on the left \n" if self.boat==LEFT else "\n Boat on the right \n"
        txt += "Farmer on the left \n" if self.farmer_on_left == 1 else "Farmer on the right \n"
        txt += "Fox on the left \n" if self.fox_on_left==1 else "Fox on the right \n"
        txt += "Chicken on the left \n" if self.chicken_on_left==1 else "Chicken on the right \n"
        txt += "Grain on the left \n" if self.grain_on_left==1 else "Grain on the right \n"
        return txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        return State(old = self)
    
    def can_move(self, F, f, c, g):
        '''Tests whether it's legal to move the boat and take
        objects.'''
        side = self.boat

        # Farmer must be on raft
        if F != 1: return False

        # Illegal moves
        # Check if Farmer is moving, he does not leave any illegal combinations
        if c == f == g == 0 and F == 1:
            # Fox and chicken can not be left alone
            if self.fox_on_left == self.chicken_on_left: return False 
            # Chicken and grain can not be left alone
            if self.chicken_on_left == self.grain_on_left: return False

        # Check if fox is moving, there are no illegal combos
        if f == 1:
            # Farmer must be on the same side as fox to move it
            if self.farmer_on_left != self.fox_on_left: return False

            # chicken cannot be alone with grain
            if self.chicken_on_left == self.grain_on_left: return False

        # Check if grain is moving there are no illegal combos
        if g == 1:
            # Farmer must be on the same side as grain
            if self.farmer_on_left != self.grain_on_left: return False

            # Chicken can not be alone with fox
            if self.chicken_on_left == self.fox_on_left: return False

        # When chicken is moving, must be on same side as farmer
        if c == 1:
            if self.farmer_on_left != self.chicken_on_left: return False

        return True
    
    def move(self, F, f, c, g):
        news = self.copy()

        if self.boat == LEFT:
            # Moving from left to right
            news.farmer_on_left -= F
            news.fox_on_left -= f
            news.chicken_on_left -= c
            news.grain_on_left -= g
        else:
            # Moving from right to left
            news.farmer_on_left += F
            news.fox_on_left += f
            news.chicken_on_left += c
            news.grain_on_left += g

        news.boat = 1 - self.boat
        return news

    def is_goal(self):
        if self.farmer_on_left == self.fox_on_left == self.chicken_on_left == self.grain_on_left == 0:
            return True
        return False
    
def goal_message(s):
    return "You did it!!!!"
        

# Put your INITIAL STATE section here.
CREATE_INITIAL_STATE = lambda : State()

# Put your OPERATORS section here.

class Operator:
    #pass
    def __init__(self, name, precond, state_transf):
       self.name = name
       self.precond = precond
       self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# etc.

combinations = [(1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
OPERATORS = [
        Operator(
            "Cross the creek with farmer and "+str(f)+" fox or "+str(c)+" chicken or "+str(g)+" grain",
            lambda s, F1=F, f1=f, c1=c, g1=g: s.can_move(F1, f1, c1, g1),
            lambda s, F1=F, f1=f, c1=c, g1=g: s.move(F1, f1, c1, g1)
            )
        for (F, f, c, g) in combinations
        ]

# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.

#<GOAL_TEST>
GOAL_TEST = lambda s: s.is_goal()
#</GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
