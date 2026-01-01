"""
DQN PSEUDOCODE
1. epsilon greedy sample from action space
2. observe what happens (next state, rewards, terminated, etc.)
3. store what we saw in the replay buffer
4. randomly sample a batch from the replay buffer (so samples are not so correlated / close together in time)
5. train the Q-network while keeping the target network stable (so there is not a "moving goalpost" and the Q-network has a chance to learn with stable
future predictions)
6. replace Q-network with target network
"""

INPUT_STATES = 4
POSSIBLE_ACTIONS = 14

class QNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(INPUT_STATES, 120), # input observation state is 4
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, POSSIBLE_ACTIONS),
        )

    def forward(self, x):
        return self.network(x)
    

if __name__ == "__main__":

    q_network = QNetwork()

    GLOBAL_STEPS = 1000
    TARGET_NETWORK_UPDATE_FREQUENCY = 1000

    replay_buffer = []

    for _ in range(GLOBAL_STEPS):
        pass
  
       
    