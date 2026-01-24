from custom_types import GamePosition, Actions, Move

class GameState:
    def __init__(self, player1_turn: bool = True, player1_hands: tuple[int, int] = (1, 1), player2_hands: tuple[int, int] = (1, 1)):
        self.player1_turn = player1_turn
        self.player1_hands = player1_hands
        self.player2_hands = player2_hands

    def move(self, move: Move):
        action, action_params = move

        if action == Actions.tap:
            attacking_hand_index = action_params[0]
            target_hand_index = action_params[1]

            if self.player1_turn:
                attacking_num = self.player1_hands[attacking_hand_index]
                target_num = self.player2_hands[target_hand_index]

                new_target_num = (target_num + attacking_num) % 5
                other_hand = self.player2_hands[1 - target_hand_index]
                self.player2_hands = (min(new_target_num, other_hand), max(new_target_num, other_hand))

            else:
                attacking_num = self.player2_hands[attacking_hand_index]
                target_num = self.player1_hands[target_hand_index]

                new_target_num = (target_num + attacking_num) % 5
                other_hand = self.player1_hands[1 - target_hand_index]
                self.player1_hands = (min(new_target_num, other_hand), max(new_target_num, other_hand))
        
        if action == Actions.split:
            new_hand_1 = action_params[0]
            new_hand_2 = action_params[1]
            if self.player1_turn:
                self.player1_hands = (new_hand_1, new_hand_2)
            else:
                self.player2_hands = (new_hand_1, new_hand_2)
                
            
        # change to next turn
        self.player1_turn = not self.player1_turn

    
    def is_valid_move(self, move: Move):
        action, action_params = move

        if action not in [Actions.tap, Actions.split]:
            raise ValueError("Invalid action. Must be 'tap' or 'split'.")
        
        if action == Actions.tap:
            attacking_hand_index = action_params[0]
            target_hand_index = action_params[1]

            if self.player1_turn:
                attacking_num = self.player1_hands[attacking_hand_index]
                target_num = self.player2_hands[target_hand_index]
            else:
                attacking_num = self.player2_hands[attacking_hand_index]
                target_num = self.player1_hands[target_hand_index]

            if attacking_num == 0:
                print(f'Attacking with an empty hand index {attacking_hand_index}')  
                return False

            if target_num == 0:
                print(f'Target is an empty hand index {target_hand_index}')  
                return False

            
        if action == Actions.split:
            hand1, hand2 = action_params

            if not (0<=hand1<=4 and 0<=hand2<=4):
                print('Distributed values must be in between [0, 4]')  
                return False

            current_hand = self.player1_hands if self.player1_turn else self.player2_hands

            if (sum(current_hand))!=sum(action_params):
                print(f'Starting and ending of distribution must be equal. {sum(current_hand)}!={sum(action_params)}')  
                return False

            if sorted(current_hand) == sorted(action_params):
                print('No duplicate swapping')  
                return False

        return True

    def is_over(self):

        if sum(self.player1_hands) == 0:
            print('Player Two Wins!')
            return True
        if sum(self.player2_hands) == 0:
            print('Player One Wins!')
            return True

        return False

    def getState(self) -> GamePosition:
        return ()

    def __repr__(self) -> str:
        output = "P1 turn" if self.player1_turn else "P2 turn"
        output += f' Player 1 hands: {self.player1_hands} Player 2 hands: {self.player2_hands}'
        return output


# handlers are written from the hero's turn point of view 
def move_handler(move: Move, game_position: GamePosition) -> GamePosition:
    param1, param2 = move[1]
    if move[0] == Actions.tap:
        return handle_tap(param1, param2, game_position)
    elif move[0] == Actions.split:
        return handle_split(param1, param2, game_position)

def handle_tap(attacking_hand_index: int, target_hand_index: int, game_position: GamePosition) -> GamePosition:

    hero_hands = game_position[0]
    villain_hands = list[int](game_position[1])

    attacking_num = hero_hands[attacking_hand_index]
    target_num = villain_hands[target_hand_index]
    
    assert attacking_num != 0, f'Attacking with an empty hand index {attacking_hand_index}'
    assert target_num != 0, f'Target is an empty hand index {target_hand_index}'
    
    new_target_num = (target_num + attacking_num) % 5
    villain_hands[target_hand_index] = new_target_num
    
    return (hero_hands, (villain_hands[0], villain_hands[1]))

def handle_split(hand1: int, hand2: int, game_position: GamePosition) -> GamePosition:
    assert 0 <= hand1 <= 4 and 0 <= hand2 <= 4, 'Distributed values must be in between [0, 4]'
    current_hand = game_position[0]
    assert sum(current_hand) == hand1 + hand2, f'Starting and ending of distribution must be equal. {sum(current_hand)}!={hand1 + hand2}'
    assert sorted(current_hand) != sorted((hand1, hand2)), 'No duplicate swapping'
    game_position = ((hand1, hand2), game_position[1])
    return game_position

