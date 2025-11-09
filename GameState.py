class GameState:
    def __init__(self, player1_turn: bool = True, low_hand: int = 1, high_hand: int = 1, opponent_low_hand: int = 1, opponent_high_hand: int = 1):
        self.player1_turn = player1_turn
        self.player1_hands = sorted([low_hand, high_hand])
        self.player2_hands = sorted([opponent_low_hand, opponent_high_hand])

    def move(self, action: str, action_params: list):
        if action == 'tap':
            attacking_hand_index = action_params[0]
            target_hand_index = action_params[1]

            if self.player1_turn:
                attacking_num = self.player1_hands[attacking_hand_index]
                target_num = self.player2_hands[target_hand_index]

                new_target_num = (target_num + attacking_num) % 5
                self.player2_hands[target_hand_index] = new_target_num

            else:
                attacking_num = self.player2_hands[attacking_hand_index]
                target_num = self.player1_hands[target_hand_index]

                new_target_num = (target_num + attacking_num) % 5
                self.player1_hands[target_hand_index] = new_target_num
        
        if action == 'split':
            new_hand_1 = action_params[0]
            new_hand_2 = action_params[1]

            if self.player1_turn:
                self.player1_hands = sorted([new_hand_1, new_hand_2])

            else:
                self.player2_hands = sorted([new_hand_1, new_hand_2])
        
        # change to next turn
        self.player1_turn = not self.player1_turn

    
    def is_valid_move(self, action: str, action_params: list):

        if action not in ['tap', 'split']:
            raise ValueError("Invalid action. Must be 'tap' or 'split'.")
        
        if action == 'tap':
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
            
        if action == "split":
            hand1, hand2 = action_params

            if not (0<hand1<=5 and 0<hand2<=5):
                print('Distributed values must be in between 0<x<=5')  
                return False
            
            current_hand = self.player1_hands if self.player1_turn else self.player2_hands

            if (current_hand)!=sum(action_params):
                print(f'Starting and ending of distribution must equal. {current_hand}!={sum(action_params)}')  
                return False
            

        return True
    



def main():
    pass