def generate_all_possible_moves(hero_state: tuple[int, int], opponent_state: tuple[int, int]):

    pass

def generate_all_distribute_moves(hero_state: tuple[int, int]):
    hero_state = (min(hero_state), max(hero_state))
    total = sum(hero_state)
    one_hand_min = max(0, total-4)
    # calculating the possible distribution positions excluding the original
    output = [(a, total-a) for a in range(one_hand_min, total//2+1) if a!=hero_state[0]]
    return output

