#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json.encoder import INFINITY
import math # This is for custom_epsilon function
from typing import Tuple, Callable, List

import toh_mdp as tm

# Partnership? YES
# Submitting partner: Yining Wei
# Other partner: Hiba Abbas
def value_iteration(
        mdp: tm.TohMdp, v_table: tm.VTable
) -> Tuple[tm.VTable, tm.QTable, float]:
    """Computes one step of value iteration.

    Hint 1: Since the terminal state will always have value 0 since
    initialization, you only need to update values for nonterminal states.

    Hint 2: It might be easier to first populate the Q-value table.

    Args:
        mdp: the MDP definition.
        v_table: Value table from the previous iteration.

    Returns:
        new_v_table: tm.VTable
            New value table after one step of value iteration.
        q_table: tm.QTable
            New Q-value table after one step of value iteration.
        max_delta: float
            Maximum absolute value difference for all value updates, i.e.,
            max_s |V_k(s) - V_k+1(s)|.
    """
    # These two are for copying the previous v_table and initialize q_table for safe modification
    new_v_table: tm.VTable = v_table.copy()
    q_table: tm.QTable = {}
    # noinspection PyUnusedLocal
    max_delta = 0.0
    # *** BEGIN OF YOUR CODE ***
    """
    In short: this method is used for updating the v_table, q_table and max_delta
    q_table stores all Q-values by pair, which will be used for chosing the acaton V

    v_table stores the best possible value for each state. It is calculated based on q_table.

    max_delta is used for checking if the value is not updating. It is used for setting a stopping condition for
    approximate the optimal value function for Value Iteration Solver, line 80 in solvers.py
    """
    # Step 1: Loop over all nonterminal states.
    for state in mdp.nonterminal_states :
        max_q_value = -INFINITY
        #Step 2: Compute Q values
        for action in mdp.actions :
            q_value = 0 #Initialize Q(s,a)
            for next_state in mdp.all_states :
                # Probability of transitioning to state next_state given that the agent takes action 'action' from state 'state'
                #P(s'|s,a)
                transition_prob = mdp.transition(state, action, next_state)
                # Reward, the immediate reward received when transitioning from state 'state' to 'next_state' by taking action 'action'
                #R(s,a,s')
                reward = mdp.reward(state, action, next_state)
                # Bellman equation
                q_value += transition_prob * (reward + mdp.config.gamma * v_table[next_state])
                # next_state loop ends
                
            q_table[(state, action)] = q_value  # Store computed Q(s, a)
            max_q_value = max(max_q_value, q_value)  # Track max Q(s, a)
            # action loop ends

        new_v_table[state] = max_q_value  # Step 3: Update V(s)
        max_delta = max(max_delta, abs(new_v_table[state] - v_table[state]))  # Step 4: Track convergence
    # ***  END OF YOUR CODE  ***
    return new_v_table, q_table, max_delta


def extract_policy(
        mdp: tm.TohMdp, q_table: tm.QTable
) -> tm.Policy:
    """Extract policy mapping from Q-value table.

    Remember that no action is available from the terminal state, so the
    extracted policy only needs to have all the nonterminal states (can be
    accessed by mdp.nonterminal_states) as keys.

    Args:
        mdp: the MDP definition.
        q_table: Q-Value table to extract policy from.

    Returns:
        policy: tm.Policy
            A Policy maps nonterminal states to actions.
    """
    # *** BEGIN OF YOUR CODE ***
    """
    In short, this method is used for choosing the best action for each nonterminal state
    given a Q-value table.
    Idea:   Step 1: Initialize an empty policy dictionary;
            Step 2: Loop over all nonterminal states;
            Step 3: For each state, find the action that gives the highest Q-value;
            Step 4: Store this action in the policy dictionary;
            Step 5: Return the final policy.
    
    Step 2 and 3 seems can be integrated into one nested loop
    """
    # Step 1: Initialize
    policies: tm.Policy = {}
    # Step 2: Loop over all nonterminal states
    for state in mdp.nonterminal_states:
        best_action = None
        best_q_value = -INFINITY
        # Step 3: For each state, find the action that gives the highest Q-value
        for action in mdp.actions:
            q_value = q_table.get((state, action), -INFINITY)  # Get Q(s, a), default to -INFINITY
            if q_value > best_q_value:  # Track best action
                best_q_value = q_value
                best_action = action
        # Step 4: Store this action in the policy dictionary if not None;
        if best_action is not None:
            policies[state] = best_action
    return policies  # Step 5: Return policy

def q_update(
        mdp: tm.TohMdp, q_table: tm.QTable,
        transition: Tuple[tm.TohState, tm.TohAction, float, tm.TohState],
        alpha: float) -> None:
    """Perform a Q-update based on a (S, A, R, S') transition.

    Update the relevant entries in the given q_update based on the given
    (S, A, R, S') transition and alpha value.

    Args:
        mdp: the MDP definition.
        q_table: the Q-Value table to be updated.
        transition: A (S, A, R, S') tuple representing the agent transition.
        alpha: alpha value (i.e., learning rate) for the Q-Value update.
    """
    state, action, reward, next_state = transition
    # *** BEGIN OF YOUR CODE ***
    """
    Idea:   Step 1: Unpack the 'transition' tuple (state, action, reward, next_state);
            Step 2: Compute the best possible Q-value from next_state s';
            Step 3: Apply the Q-learning update rule to adjust Q(s,a);
            Step 4: Store the new Q(s,a) back in the q_table.
            Step 3 and Step 4 and be together
    """
    # Step 1: Unpack 'transition'
    state, action, reward, next_state = transition
    # Step 2: Compute max Q-value for next_state
    max_next_q = max(q_table.get((next_state, next_action), 0.0)
                            for next_action in mdp.actions)
    # Step 3 and Step 4: Apply Q-learning update rule and store to q_table
    q_table[(state, action)] = q_table.get((state, action), 0.0) + \
        alpha * (reward + mdp.config.gamma * max_next_q - q_table.get((state, action), 0.0))


def extract_v_table(mdp: tm.TohMdp, q_table: tm.QTable) -> tm.VTable:
    """Extract the value table from the Q-Value table.

    Args:
        mdp: the MDP definition.
        q_table: the Q-Value table to extract values from.

    Returns:
        v_table: tm.VTable
            The extracted value table.
    """
    # *** BEGIN OF YOUR CODE ***
    """
    Idea:   Step 1: Initialize an empty V-table.
            Step 2: Iterate over all non-terminal states
            Step 3: Extract the maximum Q-value for each state
            Step 4: Return the V-table.
    
    Step 2 and 3 can implemented together
    """
    # Step 1
    v_table = {}

    # Step 2
    for state in mdp.nonterminal_states: 
        max_q_value = max(
            q_table.get((state, action), 0.0)  # Default to 0 if missing
            for action in mdp.actions
        )
        # Step 3 store the q_value
        v_table[state] = max_q_value
    
    return v_table

def choose_next_action(
        mdp: tm.TohMdp, state: tm.TohState, epsilon: float, q_table: tm.QTable,
        epsilon_greedy: Callable[[List[tm.TohAction], float], tm.TohAction]
) -> tm.TohAction:
    """Use the epsilon greedy function to pick the next action.

    You can assume that the passed in state is neither the terminal state nor
    any goal state.

    You can think of the epsilon greedy function passed in having the following
    definition:

    def epsilon_greedy(best_actions, epsilon):
        # selects one of the best actions with probability 1-epsilon,
        # selects a random action with probability epsilon
        ...

    See the concrete definition in QLearningSolver.epsilon_greedy.

    Args:
        mdp: the MDP definition.
        state: the current MDP state.
        epsilon: epsilon value in epsilon greedy.
        q_table: the current Q-value table.
        epsilon_greedy: a function that performs the epsilon

    Returns:
        action: tm.TohAction
            The chosen action.
    """
    # *** BEGIN OF YOUR CODE ***
    """
    Idea:   Step 1: Find the action(s) with the highest Q-value
            Step 2: Use epsilon_greedy from solvers.py to decide whether to pick the best action or a random one
            Step 3: Return the chosen action.
    """
    # Stop case: reach the terminal
    if state == mdp.terminal:
        return "Exit"
    # Step 1
    best_q_value = -INFINITY
    best_actions = []
    for action in mdp.actions:
        q_value = q_table.get((state, action), 0.0)  # Default q_value to 0 if missing
        if q_value > best_q_value:
            # If higer q_value, reset the action list and set the new q_value
            best_q_value = q_value
            best_actions = [action]
        elif q_value == best_q_value:
            # Otherwise, just add the action
            best_actions.append(action)
    
    # Step 2 and 3 combined together
    return epsilon_greedy(best_actions, epsilon)

def custom_epsilon(n_step: int) -> float:
    """Calculates the epsilon value for the nth Q learning step.

    Define a function for epsilon based on `n_step`.

    Args:
        n_step: the nth step for which the epsilon value will be used.

    Returns:
        epsilon: float
            epsilon value when choosing the nth step.
    """
    # *** BEGIN OF YOUR CODE ***
    """
    This is the Exponential Decay version, more aggresive
    """
    min_epsilon = 0.1  # Minimum exploration rate
    decay_rate = 0.001  # Controls how fast epsilon decreases, high value scafises the efficency for stratagy
    return min_epsilon + (1.0 - min_epsilon) * math.exp(-decay_rate * n_step)


def custom_alpha(n_step: int) -> float:
    """Calculates the alpha value for the nth Q learning step.

    Define a function for alpha based on `n_step`.

    Args:
        n_step: the nth update for which the alpha value will be used.

    Returns:
        alpha: float
            alpha value when performing the nth Q update.
    """
    # *** BEGIN OF YOUR CODE ***
    """
    I choose Inverse Square Root Decay for better learning
    """
    min_alpha = 0.1  # Minimum learning rate
    return max(min_alpha, 1 / math.sqrt(n_step + 1))