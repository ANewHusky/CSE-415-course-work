"""
This file defines the Hamming Distance heuristic for the Eight Puzzle problem.
It counts the number of tiles out of place (excluding the blank tile).
"""
from EightPuzzle import *

def h(state):
    """
    Calculate the Hamming distance for the Eight Puzzle.
    Count the number of tiles out of place (excluding the blank tile).
    """
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    flat_state = [tile for row in state.b for tile in row]
    return sum(1 for i, tile in enumerate(flat_state) if tile != goal[i] and tile != 0)

# Assign the heuristic function to the problem
h = h