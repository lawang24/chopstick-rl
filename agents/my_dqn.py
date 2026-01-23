import random
import torch
import torch.nn as nn
from custom_types import GamePosition
from move_generation import return_random_move

# SETTINGS
INPUT_STATES = 4
POSSIBLE_ACTIONS = 14
GLOBAL_STEPS = 1000
TARGET_NETWORK_UPDATE_FREQUENCY = 1000
HARDCODED_EPSILON = 0.1
LEARNING_START_STEP = 100
TRAIN_FREQ = 10  # train every 10 env steps
TARGET_UPDATE_FREQ = 50  # swap train -> target NN
GAMMA_DISCOUNT = 0.99

class QNetwork(nn.Module):

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

    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(INPUT_STATES, 120),  # input observation state is 4
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, POSSIBLE_ACTIONS),
        )

    def forward(self, x:torch.Tensor):
        return self.network(x)


if __name__ == "__main__":

    q_network = QNetwork()
    target_network = q_network.copy()

    replay_buffer = []

    state: GamePosition = ((0, 0), (0, 0))

    for step in range(GLOBAL_STEPS):
        if random.uniform(0, 1) <= HARDCODED_EPSILON:
            action = return_random_move(state)
        else:
            action = q_network(state).max()

        # don't need info term
        next_state, reward, done = env.move(action)

        rb.add(obs, next_obs, action, reward, done)

        state = next_obs

        if step > LEARNING_START_STEP:

            if TRAIN_FREQ % step == 0:
                obs, next_obs, action, reward, done = rb.sample()
                with torch.no_grad():
                    if not done:
                        target_value = (
                            reward + GAMMA_DISCOUNT * target_network(next_obs).max()
                        )
                    else:
                        target_value = reward

                    loss = MSE(target_value, q_value)

            optimizer.zero_grad()  # clear optimizer gradients
            loss.backward()  # calculate new gradients
            optimizer.step()

            if TARGET_UPDATE_FREQ % step == 0:
                target_network = QNetwork.copy()

    # save game
