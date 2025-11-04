'''
<yininw3>_KInARow.py
Authors: <Wei, Yining; Abbas, Hiba>

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from asyncio.windows_events import INFINITE
from agent_base import KAgent
from game_types import State, Game_Type

AUTHORS = 'Yining Wei and Hiba Abbas' 

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Nic'
        if twin: self.nickname += '2'
        self.long_name = 'Templatus Skeletus'
        if twin: self.long_name += ' II'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is Templatus Skeletus.\n'+\
            '"An instructor" made me.\n'+\
            'Somebody please turn me into a real game-playing agent!\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=False):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       self.current_game_type = game_type
       self.playing = what_side_to_play
       
       print("Change this to return 'OK' when ready to test the method.")
       #return "Not-OK"
       return "OK"
    
    # A helper method to generate a list of all possible moves for a state
    def get_legal_moves(self, state):
        legal_moves = []
        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] == ' ':
                    legal_moves.append((row, col)) 
        return legal_moves
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        #print("code to compute a good move should go here.")
        score, new_move = self.minimax(current_state, max_ply) 

        # debugging statements, remove before submission
        print(f"Selected move: {new_move}, type: {type(new_move)}")  
        print(f"player: {current_state.whose_move}")
        
        if new_move is None: 
            print("No legal moves found!")
            return None
        
        # THIS IS NOT ALLOWED, I need to make a deep copy of the state!
        new_state = State(current_state, None)
        new_state.board[new_move[0]][new_move[1]] = current_state.whose_move  
        new_state.whose_move = 'O' if current_state.whose_move == 'X' else 'X'
        
        new_remark = "I need to think of something appropriate.\n"
        
        print("Returning from make_move")
        return [[new_move, new_state], new_remark]


    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None):
        
        default_score = 0
        best_move = None  
        
        # Base-case, reached leaf node, return its static value
        if depth_remaining == 0:
            return self.static_eval(state, self.current_game_type), None
            # return 1, best_move
            
        legal_moves = self.get_legal_moves(state)
        if not legal_moves:  
            return 0, None
            
        # Figure out if we are minimizing or maximiing
        is_minimizing = True
        if state.whose_move == 'X':
            is_minimizing = False
            
        # set base values for alpha and beta
        if is_minimizing:
            default_score = float('inf')
        else:
            default_score = float('-inf')
            
        # recursivley search each legal move for best score
        for move in legal_moves: 
            # make the move, and evaluate it
            # THIS IS NOT ALLOWED, I need to make a deep copy of the state!, but deep_copy(state)
            # thorws an error :(
            new_state = State(state, None)
            # new_state = deep_copy(state)
            new_state.board[move[0]][move[1]] = state.whose_move
            new_state.whose_move = 'O' if state.whose_move == 'X' else 'X'
            
            score, _ = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
            
            # see if this move is better, update values, and perform pruning if true
            if is_minimizing: 
                if score < default_score:
                    best_move = move  
                    default_score = score
                    
                if pruning:
                    beta = min(beta, default_score)
                    if beta <= alpha:
                        break
            else: # trying to get a higher score
                if score > default_score:
                    best_move = move 
                    default_score = score
                    
                if pruning:
                    alpha = max(alpha, default_score)
                    if beta <= alpha:
                        break
    
        return default_score, best_move  # best_move will be a tuple (row, col)
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def static_eval(self, state, game_type):
        # Added values up here! 
        board = state.board
        k = game_type.k
        rows = len(board)      
        cols = len(board[0])   
        score = 0

        # Helper function to evaluate a sequence of k
        def evaluate_sequence(seq):
            seq_str = "".join(seq)
            line_score = 0

            if "X" * k in seq_str:  # 5 X in a row
                return INFINITE
            if "O" * k in seq_str:  # 5 O in a row, similar structor below.
                return -INFINITE
            # Assign heuristic values for growing sequences
            if f"X" * (k-1) + " " in seq_str or " " + f"X" * (k-1) in seq_str:
                line_score += 10 ** 4
            if f"O" * (k-1) + " " in seq_str or " " + f"O" * (k-1) in seq_str:
                line_score -= 10 ** 4

            if f"X" * (k-2) + " " in seq_str or " " + f"X" * (k-2) in seq_str:
                line_score += 10 ** 3
            if f"O" * (k-2) + " " in seq_str or " " + f"O" * (k-2) in seq_str:
                line_score -= 10 ** 3

            if f"X" * (k-3) + " " in seq_str or " " + f"X" * (k-3) in seq_str:
                line_score += 10 ** 2
            if f"O" * (k-3) + " " in seq_str or " " + f"O" * (k-3) in seq_str:
                line_score -= 10 ** 2

            return line_score

        # Extract all k-length sequences from rows, columns, and diagonals
        def get_all_sequences(board, k):
            sequences = []

            # Rows
            for row in board:
                #for i in range(len(row)):
                for i in range(len(row) - k + 1):
                    sequences.append(row[i:i+k])

            # Columns
            for col in range(cols):
                #for i in range(rows):
                for i in range(rows - k + 1):
                    sequences.append([board[i+j][col] for j in range(k)])

            # Diagonals (Bottom-Left to Top-Right)
            for i in range(rows - k + 1):
                #for j in range(cols):
                for j in range(cols - k + 1):
                    # Get diagonal starting at (i,j)
                    diag = [board[i+x][j+x] for x in range(k)]
                    sequences.append(diag)

            # Diagonals (Top-Left to Bottom-Right)
            for i in range(k-1, rows):
                #for j in range(cols):
                for j in range(cols - k + 1):
                    # Get diagonal starting at (i,j)
                    diag = [board[i-x][j+x] for x in range(k)]
                    sequences.append(diag)

            return sequences
        
        # Evaluate
        for seq in get_all_sequences(board, k):
            score += evaluate_sequence(seq)
        return score
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances