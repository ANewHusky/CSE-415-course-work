'''
<yourUWNetID>_KInARow.py
Authors: <your name(s) here, lastname first and partners separated by ";">
  Example:  
    Authors: Abbas, Hiba; Wei, Yining

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type

from google import genai

AUTHORS = 'Hiba Abbas and Yining Wei'

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.
import random

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'Snape'
        if twin: self.nickname += '2'
        self.long_name = 'Severus Snape'
        if twin: self.long_name += ' the twin'
        self.persona = 'bland'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is Severus Snape.\n'+\
            '"An student" made me.\n'+\
            'Raise your wand and let us duel!\n'
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

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False..
        if utterances_matter:
            # pass
            # Optionally, import your LLM API here.
            # Then you can use it to help create utterances.
            
            self.AIclient = genai.Client(api_key="AIzaSyCUQ1p6OZazKBVHb6BMV6HGLkXrOul01nc")
            
           
        # Write code to save the relevant information in variables
        # local to this instance of the agent.
        # Game-type info can be in global variables.
        self.current_game_type = game_type
        self.playing = what_side_to_play
        self.opponent = opponent_nickname
        return "OK"
       
       
   
    # A helper method to generate a list of all possible moves for a state
    def get_legal_moves(self, state):
        legal_moves = []
        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] == ' ':
                    # NEED TO RETURN TUPLES, it was a list before which was causing issues
                    legal_moves.append((row, col)) 
        return legal_moves
        
    # The core of your agent's ability should be implemented here:
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        
        if use_alpha_beta:
            score, new_move = self.minimax(current_state, max_ply, pruning=True)
        else:
            score, new_move = self.minimax(current_state, max_ply) 

        # debugging statements, remove before submission
        # print(f"Selected move: {new_move}, type: {type(new_move)}")  
        # print(f"player: {current_state.whose_move}")
        
        if new_move is None: 
            print("No legal moves found!")
            return None
        
        # THIS IS NOT ALLOWED, I need to make a deep copy of the state!
        # Update: fixed
        new_state = State(current_state, current_state.board)
        new_state.board[new_move[0]][new_move[1]] = current_state.whose_move  
        new_state.whose_move = 'O' if current_state.whose_move == 'X' else 'X'
        
        new_remark = self.make_new_utterance(current_state, new_state, current_remark)
        
        # print("Returning from make_move")
        return [[new_move, new_state], new_remark]

    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None):
        
        # if pruning is passed
        if pruning:
            alpha = float('-inf') if alpha is None else alpha
            beta = float('inf') if beta is None else beta
        
        # Get legal moves first to check if we have any
        legal_moves = self.get_legal_moves(state)
        
        # Base-case, reached leaf node, return its static value
        if depth_remaining == 0:
            score = self.static_eval(state, self.current_game_type)
            return score, None
            
        # support for none case
        if not legal_moves:  
            return self.static_eval(state, self.current_game_type), None
            
        # Figure out if we are minimizing or maximizing
        is_minimizing = True
        if state.whose_move == 'X':
            is_minimizing = False
            
        # Initialize best score and move
        best_score = float('inf') if is_minimizing else float('-inf')
        best_move = legal_moves[0]  
            
        # recursively search each legal move for best score
        for move in legal_moves:
            # make the move, and evaluate it
            # THIS IS NOT ALLOWED, I need to make a deep copy of the state!
            new_state = State(state, state.board)
            new_state.board[move[0]][move[1]] = state.whose_move
            new_state.whose_move = 'O' if state.whose_move == 'X' else 'X'
            
            score, _ = self.minimax(new_state, depth_remaining - 1, pruning, alpha, beta)
            
            # Update best move if needed
            if is_minimizing and score < best_score:
                best_score = score
                best_move = move
                if pruning:
                    beta = min(beta, best_score)
            elif not is_minimizing and score > best_score:
                best_score = score
                best_move = move
                if pruning:
                    alpha = max(alpha, best_score)
            
            if pruning and beta <= alpha:
                break
    
        return best_score, best_move

    # Static evaluation function complete!!!!
    def static_eval(self, state, game_type):
        board = state.board
        k = game_type.k
        rows = len(board)      
        cols = len(board[0])   
        score = 0

        # Helper function to evaluate a single sequence of k
        def evaluate_sequence(seq):
            seq_str = "".join(seq)
            line_score = 0

            # I added this so that any immediate wins are weighted high as possible
            if "X" * k in seq_str:  # k X's in a row
                return float('inf')
            if "O" * k in seq_str:  # k O's in a row
                return float('-inf')

            # Check for unblocked k-1 sequences, should have empty space at beginging or end
            # These are second close to winning, so they have second highest weight
            if "X" * (k-1) + " " in seq_str:
                line_score += 100000  
            if "O" * (k-1) + " " in seq_str or " " + "O" * (k-1) in seq_str:
                line_score -= 100000  

            # check for unblocked k-2 sequences, should have two empty spaces in front or back
            # these are lower on weight scale
            if "X" * (k-2) + "  " in seq_str:
                line_score += 1000
            if "O" * (k-2) + "  " in seq_str or "  " + "O" * (k-2) in seq_str:
                line_score -= 1000

            # Blocking logic!
            # Figure out how many X's and O's are in the sequence
            x_count = seq_str.count("X")
            o_count = seq_str.count("O")
            space_count = seq_str.count(" ")

            # Evaluate if blocking is needed
            # opponent is one away from winning, needs to be blocked immediately
            if o_count == (k-1) and space_count == 1:  
                line_score -= 100000  
            if x_count == (k-1) and space_count == 1: 
                line_score += 100000

            return line_score

        # Extract all k-length sequences from rows, columns, and diagonals
        # And adds their scores to the board's total score
        def get_all_sequences(board, k):
            sequences = []

            # Vertical sequences
            for col in range(cols):
                for i in range(rows - k + 1):
                    col_seq = [board[i+j][col] for j in range(k)]
                    sequences.append(col_seq)    

            # Horizontal sequences
            for row in board:
                for i in range(len(row) - k + 1):
                    sequences.append(row[i:i+k])

            # Diagonals
            for i in range(rows - k + 1):
                for j in range(cols - k + 1):
                    # Diagonal down-right
                    diag1 = [board[i+x][j+x] for x in range(k)]
                    sequences.append(diag1)
                    # Diagonal up-right
                    if i + k <= rows:
                        diag2 = [board[i+k-1-x][j+x] for x in range(k)]
                        sequences.append(diag2)

            return sequences
        
        # Evaluate those bad bois
        for seq in get_all_sequences(board, k):
            score += evaluate_sequence(seq)

        return score
    
    # This is a work in progress!
    def make_new_utterance(self, old_state, new_state, current_remark):
        old_score = self.static_eval(old_state, self.current_game_type)
        new_score = self.static_eval(new_state, self.current_game_type)
        min = False

        # list of responses
        neutral_responses = [
            "Hmph",
            "Obviously",
            "Would you like a few moments to compose a move?",
        ]
        losing_responses = [
            "I may vomit.",
            "You don't want me as your enemy, " + self.opponent + "!",
            "Obviously, you have been practicing… or cheating.",
            "I suppose even you can get lucky once in a while."
        ]
        winning_responses = [
            "Well, it may have escaped your notice," + self.opponent + ", but life isn't fair.",
            "Surely, you can do better than this?",
            "You flail like a first-year attempting their first spell.",
            "You seem to be losing, because you are neither special nor important" + self.opponent + ".",
            "How extraordinarily bad you are, " + self.opponent + ".",
        ]
        desperate_responses = [
            "I may vomit.",
            "*glares intensely*",
            "Obviously, you have been practicing… or cheating.",
            "I smell a cheater, " + self.opponent + ".",
        ]
        winning_good_responses = [
            "Can you even tell the difference between alpha beta pruning and guesswork, " + self.opponent + "?",
            "A five-year-old could have done better than that, " + self.opponent + ".",
            "If you play like this you will find yourself to be easy prey for the dark lord"
            "Seems you could use six years of magical education, " + self.opponent + ".",
        ]
        side = self.playing
        if side == 'O':
            min = True

        # Helper function to maje sure new response is not the same as current one
        def get_unique_response(responses):
            # Filter out the current remark if it's in the responses
            available_responses = [r for r in responses if r != current_remark]
            # If all responses were filtered out, use original list
            if not available_responses:
                available_responses = responses
            return random.choice(available_responses)

        # neutral
        if old_score == new_score:
            # return get_unique_response(neutral_responses)
            try: 
                return self.AIclient.models.generate_content(
                    model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                    ". And your side is " + self.playing + "with your opponent: " + self.opponent.__str__() +
                    ". You are not making progress. Give short neutral feedback based on the opponent's feedback: " + current_remark.__str__() + 
                    " and the board: " + new_state.board.__str__()
                ).text
            except:
                return get_unique_response(neutral_responses)

        
            # losing compared to previous states as O
        elif old_score < new_score and min:
            if abs(old_score - new_score) > 10000:
                #return get_unique_response(desperate_responses)
                try: 
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + " with " + self.opponent + 
                        "and you are losing badly. Give short desperate feedback based on the opponent's feedback: " + current_remark.__str__() +
                        " and the board: " + new_state.board.__str__()
                    ).text
                except:
                    return get_unique_response(desperate_responses)
            else:
                # return get_unique_response(losing_responses)
                try:
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + " with " + self.opponent + 
                        "and you are losing. Give short losing feedback based on the opponent's feed back: "+ current_remark.__str__() +
                        " and the board: " + new_state.board.__str__()
                    ).text
                except: return get_unique_response(losing_responses)
        # losing compared to previous states as X
        elif old_score > new_score and not min:
            if abs(old_score - new_score) > 10000:
                #return get_unique_response(desperate_responses)
                try:
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". Your side is " + self.playing + " with " + self.opponent + 
                        "and you are losing badly. Give desperate feedback based on the opponent's feedback: " + current_remark.__str__() +
                        "and the board: " + new_state.board.__str__()
                    ).text
                except:return get_unique_response(desperate_responses)
            else:
                #return get_unique_response(losing_responses)
                try:
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". Your side is " + self.playing + " with " + self.opponent + 
                        "and you are losing. Give losing feedback based on the opponent's feedback:" + current_remark.__str__() +
                        "and the board: " + new_state.board.__str__()
                    ).text
                except: return get_unique_response(losing_responses)
        
        # Winning compared to previous states as O
        elif old_score > new_score and min:
            # winning by a lot, probably not going to happen RIP
            if abs(old_score - new_score) > 10000:
                # return get_unique_response(winning_good_responses)
                try:
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + "with your opponent: " + self.opponent.__str__() +
                        ". You are winning good. Give short winning good feedback based on the opponent's feedback: " + current_remark.__str__() + 
                        " and the board: " + new_state.board.__str__()
                    ).text
                except: return get_unique_response(winning_good_responses)
            else:
                # return get_unique_response(winning_responses)
                try:
                    return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + "with your opponent: " + self.opponent.__str__() +
                        ". You are winning. Give short winning feedback based on the opponent's feedback: " + current_remark.__str__() + 
                        " and the board: " + new_state.board.__str__()
                    ).text
                except: return get_unique_response(winning_responses)
        # Winning compared to previous states as X
        elif old_score < new_score and not min:
            # return get_unique_response(winning_good_responses)
            try:
                return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + "with your opponent: " + self.opponent.__str__() +
                        ". You are winning good. Give short winning good feedback based on the opponent's feedback: " + current_remark.__str__() + 
                        " and the board: " + new_state.board.__str__()
                    ).text
            except: return get_unique_response(winning_good_responses)
        else:
            # return get_unique_response(neutral_responses)
            try:
                return self.AIclient.models.generate_content(
                        model="gemini-2.0-flash", contents="Pretending you are Severus Snape playing " + self.current_game_type.__str__() +
                        ". And your side is " + self.playing + "with your opponent: " + self.opponent.__str__() +
                        ". You are winning. Give short winning feedback based on the opponent's feedback: " + current_remark.__str__() + 
                        " and the board: " + new_state.board.__str__()
                    ).text
            except: return get_unique_response(neutral_responses)
        
            
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances