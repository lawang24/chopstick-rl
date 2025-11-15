from constants import Actions

class GameState:
    def __init__(self, player1_turn: bool = True, player1_hands: tuple[int, int] = (1, 1), player2_hands: tuple[int, int] = (1, 1)):
        self.player1_turn = player1_turn
        self.player1_hands = player1_hands
        self.player2_hands = player2_hands

    def move(self, action: str, action_params: tuple[int, int]):

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

    
    def is_valid_move(self, action: str, action_params: tuple[int, int]):

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

    def __repr__(self) -> str:
        output = "P1 turn" if self.player1_turn else "P2 turn"
        output += f' Player 1 hands: {self.player1_hands} Player 2 hands: {self.player2_hands}'
        return output

