import random
import math

class MinimaxAgent:
    '''
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state

        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        # Terminal test
        if state.is_full():
            return state.utility()

        maxval = -math.inf
        minval = math.inf
        for move, child in state.successors():
            val = self.minimax(child)
            maxval = max(maxval, val)
            minval = min(minval, val)

        return maxval if state.next_player() == 1 else minval
'''
class MinimaxPruneAgent(MinimaxAgent):
    '''
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent does not use a depth limit like MinimaxHeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        a = -math.inf
        b = math.inf

        return self.prune_helper(a, b, state)
    

    def prune_helper(self, a, b, state):
        # Terminal test
        if state.is_full():
            return state.utility()
        
        maxval = -math.inf
        minval = math.inf
        for move, child in state.successors():
            val = self.prune_helper(a, b, child)
            maxval = max(maxval, val)
            minval = min(minval, val)

            if state.next_player() == 1: # I am MAX
                if maxval >= b:
                    return maxval
                a = max(a, maxval)
            else:
                if minval <= a:
                    return minval
                b = min(b, minval)
                         
        return maxval if state.next_player() == 1 else minval
    '''