import random
from GameState import GameState
from action_generation import generate_all_distribute_moves, generate_all_tapping_moves

def human_turn(game: GameState):
    while True:
        user_input = input('Insert action type, param1, and param 2 \n').split()
        if (len(user_input)!=3):
            print('Invalid input, must be three')
            continue
        move_type, param1, param2 = user_input
        param1, param2 = int(param1), int(param2)

        if game.is_valid_move(move_type, (param1, param2)):
            game.move(move_type, (param1, param2))
            return
        
def computer_turn(game: GameState):

    all_possible_moves = generate_all_distribute_moves(game.player2_hands) + generate_all_tapping_moves(game.player2_hands, game.player1_hands)
    move_type, (param1, param2) = random.choice(all_possible_moves)

    print(f"Computer moves: {move_type} {param1} {param2}")

    assert game.is_valid_move(move_type, (param1, param2))
    game.move(move_type, (param1, param2))


def main():
    
    game = GameState(player1_turn=False, player1_hands=(0, 4), player2_hands=(1, 1))
    while (not game.is_over()):
        print(game)
        if game.player1_turn:
            human_turn(game)
        else:
            computer_turn(game)
        print()

if __name__ == "__main__":
    main()