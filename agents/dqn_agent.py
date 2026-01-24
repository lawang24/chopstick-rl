from sympy.physics.mechanics.tests.test_actuator import target
import GameState
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from custom_types import GamePosition, Move, ReplayBufferElement
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
SEED = 2 # deterministic seed for reproduction
RB_BATCH_SIZE = 10


def gamePositionToTensor(game_position: GamePosition)-> torch.Tensor:
    return torch.tensor(game_position).flatten()

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

    torch.manual_seed(SEED)

    q_network = QNetwork()

    # copy over target network to start
    target_network = QNetwork()
    target_network.load_state_dict(q_network.state_dict())

    replay_buffer: list[ReplayBufferElement] = []
    state: GamePosition = ((0, 0), (0, 0))

    optimizer = torch.optim.Adam(q_network.parameters())

    for step in range(GLOBAL_STEPS):
        if random.uniform(0, 1) <= HARDCODED_EPSILON: # exploration
            action: Move = return_random_move(state)
        else: # exploitation
            # TODO: convert q_network output into a move
            action = q_network(gamePositionToTensor(state))

        post_dqn_move: GamePosition =  GameState.move_handler(action, state)
        reward = 0
        # won the game
        if sum(post_dqn_move[1]) == 0: 
            # +1 reward for victory
            replay_buffer.append({"old_state": state, "next_state": "terminal", "action": action, "reward": 1})
            state = ((0, 0), (0, 0))
        # game didn't end, so now it's opponent's turn to move
        else:
            opponent_view: GamePosition = post_dqn_move[::-1]
            # opponent does a random move
            opponent_view: GamePosition = GameState.move_handler(return_random_move(opponent_view), opponent_view) 
            # if opponent wins, negative reward
            if sum(opponent_view[1]) == 0:
                reward = -1
                replay_buffer.append({"old_state": state, "next_state": "terminal", "action": action, "reward": -1})
                state = ((0, 0), (0, 0))
            else:
                # game continues, no one has won
                state: tuple[tuple[int, int], tuple[int, int]] = opponent_view[::-1]
                replay_buffer.append({"old_state": state, "next_state": state, "action": action, "reward": 0})

        if step > LEARNING_START_STEP:
            if TRAIN_FREQ % step == 0:

                # how many should I sample
                samples = random.sample(replay_buffer, RB_BATCH_SIZE )

                # iterate through the samples for now

                for sample in samples:
                    reward = sample["reward"]
                    old_state = sample["old_state"]
                    next_state = sample["next_state"]
                    action = sample["action"]
                    # terminal state with reward
                    if next_state == 'terminal':
                        target_value = torch.tensor(reward)
                    else:
                        target_value = (
                            reward + GAMMA_DISCOUNT * target_network(next_state).max()
                        )

                    current_q_value = q_network(old_state).max()

                    loss = F.mse_loss(current_q_value, target_value)

                    optimizer.zero_grad()  # clear optimizer gradients
                    loss.backward()  # calculate new gradients
                    optimizer.step()

            if TARGET_UPDATE_FREQ % step == 0:
                target_network = QNetwork.copy()

    # save game
