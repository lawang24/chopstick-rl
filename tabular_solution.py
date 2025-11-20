from state_generation import generate_all_states_ordered, poss_hands
from action_generation import generate_all_possible_moves
from custom_types import game_position
from constants import Actions
from GameState import handle_tap, handle_split
from math import inf

def calculate_value(curr_game_pos: game_position, rewards: dict[game_position, int]):
    all_possible_moves = generate_all_possible_moves(curr_game_pos[0], curr_game_pos[1])
    champ = -inf
    for move_type, (param1, param2) in all_possible_moves:
        if move_type == Actions.tap:
            new_game_pos = handle_tap(param1, param2, curr_game_pos)
        elif move_type == Actions.split:
            new_game_pos = handle_split(param1, param2, curr_game_pos)

        # flip positions to show diff turn
        new_game_pos = (new_game_pos[1], new_game_pos[0])

        if new_game_pos not in rewards:
            # hold with 0, may be overwritten later
            rewards[new_game_pos] = 0
            calculate_value(new_game_pos, rewards)
        
        # best action for this turn is the worst reward for your opponent's next move 
        # NEGAMAX IMPLEMENTATION
        champ = max(champ, -rewards[new_game_pos])

    rewards[curr_game_pos] = champ

    return rewards[curr_game_pos]
        

# GOAL: 
# +1 for guaranteed victory, 0 for cycle potential, 1 for loss
def minimax_solution():

    # doubles as a visited array
    # always positioned as player 1's turn
    reward: dict[game_position, int] = {}

    for my_hand in poss_hands:
        for opp_hand in poss_hands:
            if my_hand == (0, 0):
                reward[(my_hand, opp_hand)] = -1
            if opp_hand == (0, 0):
                reward[(my_hand, opp_hand)] = 1

    del reward[(0, 0), (0, 0)]

    all_possible_states = generate_all_states_ordered()
    for game_pos in all_possible_states:
        if game_pos not in reward:
            reward[game_pos] = calculate_value(game_pos, reward)

    for game_pos in all_possible_states:
        print(game_pos, reward[game_pos])


if __name__ == "__main__":
    minimax_solution()