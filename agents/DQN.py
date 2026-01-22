import numpy as np
from custom_types import GamePosition, Move
import torch.nn as nn

GAME_STATE_OBS = 4
# tapping: 4 actions + 
# distributing: max of 5 (transferred) * 2 (symmetry)
POSSIBLE_ACTIONS = 14

# trains by learning against a random agent
# 
class DQN_AGENT:
    def __init__(self):
        # input vector GamePosition 
        # output vector of positions
        self.DQN = DQN(4,  14)
        
        

    def get_move(self, position: GamePosition) -> Move:
        """Generates a move given a GamePosition."""
        pass

    def train():
        pass


# 1. train by playing against the random agent
# inference for DQN_AGENT will be after DQN_AGENT.train(), then
# no replay buffer for now

class DQN(nn.Module):
    def __init__(self, n_obs, n_actions):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(n_obs, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, n_actions)
        )
    
    def forward(self, x):
        return self.network(x)



