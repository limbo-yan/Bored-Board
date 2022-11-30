from __future__ import print_function
import pickle
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy
# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras

import serial
import time

class Human(object):
    """
    human player
    """

    def __init__(self, arduino):
        self.player = None
        self.arduino = arduino

    def get_val_from_arduino(self):
        data = self.arduino.readline()
        while data == bytes('', 'utf-8'):
            data = self.arduino.readline()
        data = data.decode("utf-8")
        time.sleep(0.5)
        return data

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = self.get_val_from_arduino()
            print(location)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            # print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)
      

def run():
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)
    n = 5
    width, height = 8, 8
    # model_file = 'best_policy_3_3_3_pytorch100.model'
    # model_file = 'best_policy_8_8_5_pytorch950.model'
    model_file = 'best_policy_8_8_5.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board, arduino)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        # '''
        try:
            policy_param = pickle.load(open(model_file, 'rb'))
        except:
            policy_param = pickle.load(open(model_file, 'rb'),
                                       encoding='bytes')  # To support python3
        best_policy = PolicyValueNetNumpy(width, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance
        # '''
        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human(arduino)

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=0, is_shown=1)

        # two players
        # game.start_play(human, human, start_player=0, is_shown=1)
        
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
