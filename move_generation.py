from custom_types import Actions, Move
import random

def generate_all_tapping_moves(hero_state: tuple[int, int], opponent_state: tuple[int, int]) -> list[Move]:
    moves: list[Move] = []
    for i, h1 in enumerate[int](hero_state):
        for j, h2 in enumerate[int](opponent_state):
            if h1 and h2:
                moves.append((Actions.tap, (i, j)))
    return moves

def generate_all_distribute_moves(hero_state: tuple[int, int]) -> list[Move]:
    hero_state = (min(hero_state), max(hero_state))
    total = sum(hero_state)
    one_hand_min = max(0, total-4)
    # calculating the possible distribution positions excluding the original
    output: list[Move] = [(Actions.split,(a, total-a)) for a in range(one_hand_min, total//2+1) if a!=hero_state[0]]
    return output

def generate_all_possible_moves(hero_state: tuple[int, int], opponent_state: tuple[int, int]) -> list[Move]:
    return generate_all_distribute_moves(hero_state) + generate_all_tapping_moves(hero_state, opponent_state)

def return_random_move(hero_state: tuple[int, int], opponent_state: tuple[int, int]) -> Move:
    all_possible_moves = generate_all_possible_moves(hero_state, opponent_state)
    random_move: Move = random.choice(all_possible_moves)
    return random_move

