#!/usr/bin/python3
""" ItrBFS.py
Student Names: Yining Wei, Hiba Abbas
UW NetIDs:yininw3, hibaa3
CSE 415, Winter, 2025, University of Washington

This code contains my implementation of the Iterative BFS algorithm.

Usage:
 python ItrBFS.py HumansRobotsFerry
"""

import sys
import importlib


class ItrBFS:
    """
    Class that implements Iterative BFS for any problem space (provided in the required format)
    """

    def __init__(self, problem):
        """ Initializing the ItrBFS class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded
        self.MAX_OPEN_LENGTH = None  # Maximum length of the open list
        self.PATH = None  # Solution path
        self.PATH_LENGTH = None  # Length of the solution path
        self.BACKLINKS = None  # Predecessor links, used to recover the path
        print("\nWelcome to ItrBFS")

    def runBFS(self):
        # Comment out the line below when this function is implemented.
        #raise NotImplementedError
        """This is an encapsulation of some setup before running
        BFS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.IterativeBFS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")
    
    def IterativeBFS(self, initial_state):
        #Import the deque
        from collections import deque

        # Initialize the queue for OPEN and the CLOSED list, inspired by step 1
        OPEN = deque([initial_state])
        CLOSED = []
        self.BACKLINKS[initial_state] = None

        #If OPEN is empty, output “DONE” and stop.
        while OPEN:
            self.MAX_OPEN_LENGTH = max(self.MAX_OPEN_LENGTH, len(OPEN))
            print(f"OPEN length: {len(OPEN)}, CLOSED length: {len(CLOSED)}")

            # Dequeue the front state, inspire by a part of step 3
            S = OPEN.popleft()
            CLOSED.append(S)

            # Check if goal state, inspired by step 3
            if S.is_goal():
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f"Length of solution path found: {self.PATH_LENGTH} edges")
                return
            self.COUNT += 1

            # Generate successors of the current state, inspired by step 4 of DFS
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    if new_state not in CLOSED and new_state not in OPEN:
                        OPEN.append(new_state)
                        self.BACKLINKS[new_state] = S
            print_state_list("OPEN", list(OPEN))

        print("No solution found.")

    """This method is used for backtracing the path to get the answer
    Returns the path
    """
    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path


#The following methods are copied from IterDFS
def print_state_list(lst_name, lst):
    """
    Prints the states in lst with name lst_name
    """
    print(f"{lst_name} is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        Problem = sys.argv[1]
    BFS = ItrBFS(Problem)
    BFS.runBFS()
