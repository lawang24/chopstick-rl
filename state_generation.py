poss_hands = [(a, b) for a in range(5) for b in range(5)]

def generate_all_states_ordered() -> list[tuple[int, int]]:
    # remove ((0, 0), (0,0)) impossible state
    return [(a, b) for a in poss_hands for b in poss_hands if sum(a+b) != 0]

if __name__ == "__main__":
    all_poss = generate_all_states_ordered() 
    print(all_poss)