from custom_types import Actions, Move, GamePosition
import random

def generate_all_tapping_moves(game_position: GamePosition) -> list[Move]:
    hero_state = game_position[0]
    opponent_state = game_position[1]
    moves: list[Move] = []
    for i, h1 in enumerate[int](hero_state):
        for j, h2 in enumerate[int](opponent_state):
            if h1 and h2:
                moves.append((Actions.tap, (i, j)))
    return moves

def generate_all_distribute_moves(game_position: GamePosition) -> list[Move]:
    hero_state = game_position[0]
    hero_state = (min(hero_state), max(hero_state))
    total = sum(hero_state)
    one_hand_min = max(0, total-4)
    # calculating the possible distribution positions excluding the original
    output: list[Move] = [(Actions.split,(a, total-a)) for a in range(one_hand_min, total//2+1) if a!=hero_state[0]]
    return output

def generate_all_possible_moves(game_position: GamePosition) -> list[Move]:
    return generate_all_distribute_moves(game_position) + generate_all_tapping_moves(game_position)

def return_random_move(game_position: GamePosition) -> Move:
    all_possible_moves = generate_all_possible_moves(game_position)
    random_move: Move = random.choice(all_possible_moves)
    return random_move

