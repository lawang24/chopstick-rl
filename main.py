from GameState import GameState

def human_turn(game: GameState):
    while True:
        user_input = input('Insert action type, param1, and param 2 \n').split()
        if (len(user_input)!=3):
            print('Invalid input, must be three')
            continue
        move_type, param1, param2 = user_input
        param1, param2 = int(param1), int(param2)

        if game.is_valid_move(move_type, [param1, param2]):
            game.move(move_type, [param1, param2])
            return
        
def computer_turn(game: GameState):
    
    # generate all possible moves 
    # choose randomly


def main():
    
    game = GameState()
    while (not game.is_over()):
        print(game)
        # human player move
        if game.player1_turn:
            human_turn(game)
            continue

        user_input = input('Insert action type, param1, and param 2 \n').split()
        if (len(user_input)!=3):
            print('Invalid input, must be three')
            continue

        move_type, param1, param2 = user_input
        param1, param2 = int(param1), int(param2)
        if not game.is_valid_move(move_type, [param1, param2]):
            continue
        game.move(move_type, [param1, param2])

        print()
        
    
if __name__ == "__main__":
    main()