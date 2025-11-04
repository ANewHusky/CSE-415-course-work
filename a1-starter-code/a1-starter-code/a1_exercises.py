# Starter code file for A1.  Remove this line before submission to Gradescope.
# Put your name and UWNetID here, replacing this line.
# CSE 415, Assignment 1, Winter 2025.

from cmath import sqrt
import re
from collections import Counter


def is_a_quintuple(n):
    """Return True if n is a multiple of 5; False otherwise."""
    return n % 5 == 0

def last_prime(m):
    """Return the largest prime number p that is less than or equal to m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    if prime_checker(m):
        return m
    else:
        while(True):
            m = m - 1
            if prime_checker(m):
                return m

# This is the helper method for last_prime
def prime_checker(m):
    flag = True
    for i in range(2, m):
        if(m % i) == 0:
            flag = False
        
    return flag

def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    """solutionOne = (-b + sqrt((b**2 - 4*a*c))) / (2*a)
    solutionTwo = (-b - sqrt((b**2 - 4*a*c))) / (2*a)"""
    #Idealy,先判断虚实再开方，不然sqrt内部是负数时会报错
    """
    try:
        sqrt
    catch:
        return "complex"
    """
    solutionOne = (-b + ((b**2 - 4*a*c))**0.5) / (2*a)
    solutionTwo = (-b - ((b**2 - 4*a*c))**0.5) / (2*a)
    #if (not(isinstance(solutionOne, complex))) & (not(isinstance(solutionTwo, complex))):
    if(b**2 - 4*a*c) >= 0:
        #both instance, return both
        return (solutionOne, solutionTwo)
    else:
        return "complex"

def new_quadratic_function(a, b, c):
    """Create and return a new, anonymous function (for example
    using a lambda expression) that takes one argument x and 
    returns the value of ax^2 + bx + c."""
    return lambda x: a * x**2 + b*x + c


def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    Perfect shuffle means splitting a list into two halves and then interleaving
    them. For example, the perfect shuffle of [0, 1, 2, 3, 4, 5, 6, 7] is
    [0, 4, 1, 5, 2, 6, 3, 7]."""
    first_half = even_list[0:(int)(len(even_list) / 2)]
    second_half = even_list[(int)(len(even_list) / 2) : (int)(len(even_list))]
    toReturn = []
    for i in range(0, len(first_half), 1):
        toReturn.append(first_half[i])
        toReturn.append(second_half[i])
    return toReturn


def list_of_5_times_elts_plus_1(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 5 and had 1 added to it."""
    toReturn = [i * 5 + 1 for i in input_list]
    """for i in input_list:
        toReturn.append(i * 5 + 1)"""
    return toReturn

def double_vowels(text):
    """Return a new version of text, with all the vowels doubled.
    For example:  "The *BIG BAD* wolf!" => "Theee "BIIG BAAD* woolf!".
    For this exercise assume the vowels are
    the characters A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
    toReturn = []
    for char in text:
        if char in vowels:
            toReturn.append(char * 2)
        else:
            toReturn.append(char)
    return ''.join(toReturn)

def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', '*', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ] { } | : ).
    Convert all the letters to lower-case before the counting."""
    text = text.lower()
    #pattern = r"[a-zA-Z0-9\-\+\*\/\@\#\%']+"
    pattern = r"[a-zA-Z0-9\-\+\*/@#%']+"
    words = re.findall(pattern, text)
    word_counts = Counter(words)
    return dict(word_counts)

class TTT_State:
    
    def __init__(self):
        '''Create an instance. This happens to represent the initial state
        for Tic-Tac-Toe.'''
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]
        self.whose_move = 'X'

    def __str__(self):
        '''Return a string representation of the
        state that show the Tic-Tac-Toe board as a 2-D ASCII display.
        Style it simply, as you wish.'''
        rows = [f"[{' '.join(row)}]" for row in self.board]
        return "\n".join(rows)

    def __deepcopy__(self):
        '''Return a new instance with the same board arrangement 
        and player to move. 
        (Sublists must be copies, not copies of references.)'''
        from copy import deepcopy
        toReturn = self.__class__()
        toReturn.board = deepcopy(self.board)
        toReturn.whose_move = self.whose_move
        return toReturn

    def __eq__(self, other):
        '''Return True iff two states are equal.'''
        if(isinstance(other, self.__class__)):
            return self.board == other.board and self.whose_move == other.whose_move
        else:
            return False

class TTT_Operator:
    '''An instance of this class will represent an
    operator that can make a move by who (either 'X' or 'O'),
    to the given row and column. '''
    
    def __init__(self, who, row, col):
        self.who = who
        self.row = row
        self.col = col
    
    def is_applicable(self, state):
        '''Return True if it would be legal to apply
        this operator to the given state.'''
        return state.board[self.row][self.col] == " " and state.whose_move == self.who

    def apply(self, state):
        '''Return a new state object that represents the
        result of applying this operator to the given state.'''
        new_state = state.__deepcopy__()
        new_state.board[self.row][self.col] = self.who
        if self.who == 'X':
            new_state.whose_move = 'O'
        else:
            new_state.whose_move = 'X'
        #new_state.whose_move = 'O' if self.who == 'X' else 'X'   python style
        return new_state