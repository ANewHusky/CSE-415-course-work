# EightPuzzleWithManhattan.py
"""
This file defines the Total Manhattan Distance heuristic for the Eight Puzzle problem.
It calculates the sum of Manhattan distances for all tiles.
"""

from EightPuzzle import *

def h(state):
    """
    Calculate the Total Manhattan distance for the Eight Puzzle.
    Sum the vertical and horizontal distances of each tile from its goal position.
    """
    goal_positions = {0: (0, 0), 1: (0, 1), 2: (0, 2),
                      3: (1, 0), 4: (1, 1), 5: (1, 2),
                      6: (2, 0), 7: (2, 1), 8: (2, 2)}

    manhattan_distance = 0
    for i in range(3):
        for j in range(3):
            value = state.b[i][j]
            if value != 0:  # Skip the blank tile
                goal_i, goal_j = goal_positions[value]
                manhattan_distance += abs(i - goal_i) + abs(j - goal_j)
    return manhattan_distance

# Assign the heuristic function to the problem
h = h