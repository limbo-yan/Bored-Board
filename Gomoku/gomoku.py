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
            Either a board (sequence of sequences, filled with 1, -1, 0, or -2, describing game state)
            or two numbers specifying the rows, columns for a blank board
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


    