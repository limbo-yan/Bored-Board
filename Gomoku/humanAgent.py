class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        userInput = input("Kindly enter your move - e.g: 1,1: ")
        move = None
        while move not in move__state:
            try:
                move = tuple(map(int, userInput.split(',')))
            except ValueError:
                continue
        return move, move__state[move]