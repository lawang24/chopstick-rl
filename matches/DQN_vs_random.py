from agents.random_agent import RandomAgent
from agents.dqn_agent import QNetwork
from GameState import GameState

agent1 = RandomAgent()
agent2 = QNetwork()

game = GameState()

turn = 0
while not game.is_over():
    if turn % 2 == 0:
        curr_agent = agent1
    else:
        curr_agent = agent2
    
    move = curr_agent.get_move(game.get_state())
    game.make_move(move)
    
    turn += 1

# Victor had the last turn
if turn % 2 == 0:
    print("Agent2 Victory!")
else:
    print("Agent1 Victory!")