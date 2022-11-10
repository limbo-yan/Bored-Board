import argparse
from minimaxAgent import MinimaxPruneAgent
from humanAgent import HumanAgent

class GameState:
    """
    Class representing a single state of a Gomoku game.

    The board is stored as a 2D list, containing 1's representing Player 1's pieces, -1's
    for Player 2(or an AI agent), unused spaces are 0 and "obstacles" are -2.
    """   

    state_count = 0  # bookkeeping to help track how efficient agents' search methods are running

    def __init__(self, *args):
        """Constructor for Gomoku state.

        Args:
            two numbers specifying the rows, columns for a blank board
        """    
        if len(args) == 2:
            r, c = args
            self.num_rows = r
            self.num_cols = c
            self.board = tuple([ tuple([0]*self.num_cols) ]*self.num_rows)  
        else:
            board = args[0]
            self.num_rows = len(board)
            self.num_cols = len(board[0])
            self.board = tuple([ tuple(board[r]) for r in range(self.num_rows) ])

        # 1 for Player 1, -1 for Player 2
        self._next_p = 1 if (sum(sum(row) for row in self.board) % 2) == 0 else -1
        self._moves_left = sum(sum([1 if x == 0 else 0 for x in row]) for row in self.board)  

    def next_player(self):
        """Determines who's move it is based on the board state.

        Returns: 1 if Player 1 goes next, -1 if it's Player 2's turn
        """
        return self._next_p
    
    def is_full(self):
        """Checks to see if there are available moves left."""
        return self._moves_left <= 0
            
    def _create_successor(self, row, col):
        """Create the successor state that follows from a given move."""

        # Duplicate a new board from the current board
        successor_board = [ list(row) for row in self.board ]
        if (successor_board[row][col] != 0) or row >= self.num_rows or col >= self.num_cols:
            raise Exception("Illegal successor: {}, {}".format(col, self.board))
        successor_board[row][col] = self._next_p
        successor = GameState(successor_board)
        GameState.state_count += 1
        return successor
    
    def successors(self):
        """Generates successor state objects for all valid moves from this board.

        Returns: a _sorted_ list of (move, state) tuples
        """
        move_states = []
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if self.board[row][col] == 0:
                    move_states.append(((row, col), self._create_successor(row, col)))        
        return move_states
    
    def get_rows(self):
        """Return a list of rows for the board."""
        return [[c for c in r] for r in self.board]

    def get_cols(self):
        """Return a list of columns for the board."""
        return list(zip(*self.board))

    def get_diags(self):
        """Return a list of all the diagonals for the board."""
        b = [None] * (len(self.board) - 1)
        grid_forward = [b[i:] + r + b[:i] for i, r in enumerate(self.get_rows())]
        forwards = [[c for c in r if c is not None] for r in zip(*grid_forward)]
        grid_back = [b[:i] + r + b[i:] for i, r in enumerate(self.get_rows())]
        backs = [[c for c in r if c is not None] for r in zip(*grid_back)]
        return forwards + backs
    
    def __str__(self):
        symbols = { -1: "O", 1: "X", 0: "-", -2: "#" }
        s = ""
        for r in range(self.num_rows-1, -1, -1):
            s += "\n"
            s += str(r)
            for c in range(self.num_cols):
                s += "  " + symbols[self.board[r][c]]

        s += "\n "
        for c in range(self.num_cols):
            s += "  " + str(c)
        s += "\n"
        return s
    
    def is_done(self):
        '''Check if there is already a winner'''
        for run in self.get_rows() + self.get_cols() + self.get_diags():
            for elt, length in streaks(run):
                if length == 5:
                    return elt
        return 0

def streaks(lst):  
    """Get the lengths of all the streaks of the same element in a sequence."""
    rets = []  # list of (element, length) tuples
    prev = lst[0]
    curr_len = 1
    for curr in lst[1:]:
        if curr == prev:
            curr_len += 1
        else:
            rets.append((prev, curr_len))
            prev = curr
            curr_len = 1
    rets.append((prev, curr_len))
    return rets

def play_game(player1, player2, state):
    """Run a Gomoku Game"""
    print(state)
    turn = 0
    p1_state_count, p2_state_count = 0, 0
    while (not state.is_full()):
        winner = state.is_done()
        if winner == 1:
            print("Player 1 wins!")
            return 1
        elif winner == -1:
            print("Player 2 wins!")
            return -1

        player = player1 if state.next_player() == 1 else player2

        state_count_before = GameState.state_count
        move, state_next = player.get_move(state)
        state_count_after = GameState.state_count

        states_created = state_count_after - state_count_before
        if state.next_player() == 1:
            p1_state_count += states_created
        else:
            p2_state_count += states_created  

        print("Turn {}:".format(turn))        
        print("Player {} generated {} states".format(1 if state.next_player() == 1 else 2, states_created))
        print("Player {} moves to {}".format(1 if state.next_player() == 1 else 2, move))
        print(state_next) 
        
        turn += 1
        state = state_next

    print("It's a tie.")
    print("Player 1 generated {} states".format(p1_state_count))
    print("Player 2 generated {} states".format(p2_state_count))
    print("")
    return 0



################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('p1', choices=['h','c'])
    parser.add_argument('p2', choices=['h','c'])
    parser.add_argument('nrows', type=int)
    parser.add_argument('ncols', type=int)
    args = parser.parse_args()

    players = []
    for p in [args.p1, args.p2]:
        if p == 'h':
            player = HumanAgent()
        elif p == 'c':
            player = MinimaxPruneAgent()
        players.append(player)            

    
    start_state = GameState(args.nrows, args.ncols)

    play_game(players[0], players[1], start_state)