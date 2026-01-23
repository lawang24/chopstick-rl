from custom_types import Move, GamePosition
from move_generation import return_random_move

class RandomAgent:
    '''
    Always plays a random move
    '''
    def get_move(self, game_position: GamePosition) -> Move:
        return return_random_move(game_position[0], game_position[1])



        