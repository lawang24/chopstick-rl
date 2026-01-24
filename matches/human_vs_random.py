import random

from GameState import GameState
from move_generation import generate_all_distribute_moves, generate_all_tapping_moves
from custom_types import Actions

def human_turn(game: GameState):
    while True:
        user_input = input('Insert action type, param1, and param 2 \n').split()
        if (len(user_input)!=3):
            print('Invalid input, must be three')
            continue
        move_type, param1, param2 = user_input
        param1, param2 = int(param1), int(param2)
        action = Actions.tap if move_type == 'tap' else Actions.split
        move = (action, (param1, param2))

        if game.is_valid_move(move):
            game.move(move)
            return
        
def computer_turn(game: GameState):
    game_position = (game.player2_hands, game.player1_hands)
    all_possible_moves = generate_all_distribute_moves(game_position) + generate_all_tapping_moves(game_position)
    move = random.choice(all_possible_moves)
    move_type, (param1, param2) = move

    print(f"Computer moves: {move_type} {param1} {param2}")

    assert game.is_valid_move(move)
    game.move(move)


def main():
    
    game = GameState()
    while (not game.is_over()):
        print(game)
        if game.player1_turn:
            human_turn(game)
        else:
            computer_turn(game)

if __name__ == "__main__":
    main()