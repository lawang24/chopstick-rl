import GameState
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from custom_types import GamePosition, Move, ReplayBufferElement, Actions, ActionType
from move_generation import return_random_move

# SETTINGS
INPUT_STATES = 4
POSSIBLE_ACTIONS = 50
GLOBAL_STEPS = 100
TARGET_NETWORK_UPDATE_FREQUENCY = 10
HARDCODED_EPSILON = 0.1
LEARNING_START_STEP = 10
TRAIN_FREQ = 10  # train every 10 env steps
TARGET_UPDATE_FREQ = 50  # swap train -> target NN
GAMMA_DISCOUNT = 0.99
SEED = 2  # deterministic seed for reproduction
RB_BATCH_SIZE = 10


def gamePositionToTensor(game_position: GamePosition) -> torch.Tensor:
    '''
    Game Input is a 4D normalized tensor
    '''
    return torch.tensor(game_position, dtype=torch.float32).flatten()


# valid move mask will be [left_hand][right_hand][action_type]
def getValidMoveMask(game_position: GamePosition) -> torch.Tensor:
    """
    we want to map a space of all the possible moves and do one-hot encoding on the valid ones
    in a given move, you can
        1. (split) (lh) (rh) = 5 * 5 = 25 possible actions
        2. (tap) (tapping hard) (opponent hand) = 2 * 2 = 4 possible actions
    29 total action flattened space

    Will represent as a 2d mask, first dimension is move type
    second dimension is action, will pad to 25
    """
    mask = torch.zeros(2, 25)

    # generate all split moves
    hero_hand, opp_hand = game_position
    lh, rh = hero_hand

    hero_total = sum(hero_hand)
    for h1 in range(5):
        for h2 in range(5):
            if h1 + h2 == hero_total and sorted((h1, h2)) != sorted(hero_hand):
                mask[0][h1 * 5 + h2] = 1

    # generate all tap moves
    for attacking_hand in range(2):
        for target_hand in range(2):
            # hand does not exist
            if hero_hand[attacking_hand] == 0 or opp_hand[target_hand] == 0:
                continue
            mask[1][attacking_hand * 2 + target_hand] = 1

    return mask.flatten()


def mask_idx_to_action(idx: int) -> Move:
    '''
    Reverses flattened tensor -> ActionType mapping
    '''
    # split
    if idx < 25:
        return (Actions.split, (idx // 5, idx % 5))
    # tap
    idx -= 25
    return (Actions.tap, (idx // 2, idx % 2))

def action_to_idx(move: Move) -> int:
    type, (param1, param2) = move
    if type == Actions.split:
        idx = param1 * 5 + param2
    else:
        idx = 25 +  param1 * 2 + param2
    return idx


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

    def forward(self, x: torch.Tensor):
        return self.network(x)


if __name__ == "__main__":
    torch.manual_seed(SEED)

    q_network = QNetwork()

    # copy over target network to start
    target_network = QNetwork()
    target_network.load_state_dict(q_network.state_dict())

    replay_buffer: list[ReplayBufferElement] = []
    state: GamePosition = ((1, 1), (1, 1))

    optimizer = torch.optim.Adam(q_network.parameters())

    for step in range(GLOBAL_STEPS):
        if random.uniform(0, 1) <= HARDCODED_EPSILON:  # exploration
            action: Move = return_random_move(state)
        else:  # exploitation
            unmasked_actions: torch.Tensor = q_network(gamePositionToTensor(state))
            valid_move_mask = getValidMoveMask(state)
            masked_actions = unmasked_actions.masked_fill(~valid_move_mask.bool(), float('-inf'))
            action: Move  = mask_idx_to_action(masked_actions.argmax().item())

        post_dqn_move: GamePosition = GameState.move_handler(action, state)
        reward = 0
        # won the game
        if sum(post_dqn_move[1]) == 0:
            # +1 reward for victory
            replay_buffer.append(
                {
                    "old_state": state,
                    "next_state": "terminal",
                    "action": action,
                    "reward": 1,
                }
            )
            state = ((1, 1), (1, 1))
        # game didn't end, so now it's opponent's turn to move
        else:
            opponent_view: GamePosition = post_dqn_move[::-1]
            # opponent does a random move
            opponent_view: GamePosition = GameState.move_handler(
                return_random_move(opponent_view), opponent_view
            )
            # if opponent wins, negative reward
            if sum(opponent_view[1]) == 0:
                reward = -1
                replay_buffer.append(
                    {
                        "old_state": state,
                        "next_state": "terminal",
                        "action": action,
                        "reward": -1,
                    }
                )
                state = ((1, 1), (1, 1))
            else:
                # game continues, no one has won
                new_state: tuple[tuple[int, int], tuple[int, int]] = opponent_view[::-1]
                replay_buffer.append(
                    {
                        "old_state": state,
                        "next_state": new_state,
                        "action": action,
                        "reward": 0,
                    }
                )
                state = new_state

        if step > LEARNING_START_STEP:
            if step % TRAIN_FREQ   == 0:
                # how many should I sample
                samples = random.sample(replay_buffer, RB_BATCH_SIZE)

                # iterate through the samples for now

                for sample in samples:
                    reward = sample["reward"]
                    old_state = sample["old_state"]
                    next_state = sample["next_state"]
                    action = sample["action"]
                    action_idx = action_to_idx(action)
                    # terminal state with reward
                    if next_state == "terminal":
                        target_value = torch.tensor(reward, dtype=torch.float32)
                    else:
                        unmasked_actions = target_network(
                            gamePositionToTensor(next_state)
                        )
                        # need to fix masking logic
                        valid_move_mask = getValidMoveMask(next_state)
                        target_value_next_state_value: float = unmasked_actions[valid_move_mask.bool()].max()
                        # reward will almost always be zero here anyways
                        target_value = (
                            reward
                            + GAMMA_DISCOUNT
                            * target_value_next_state_value
                        )

                    current_q_value = q_network(gamePositionToTensor(old_state))[action_idx]

                    loss = F.mse_loss(current_q_value, target_value)
                    optimizer.zero_grad()  # clear optimizer gradients
                    loss.backward()  # calculate new gradients
                    optimizer.step()

            if step % TARGET_UPDATE_FREQ  == 0:
                target_network.load_state_dict(q_network.state_dict())

        print(state)
        print(len(replay_buffer))


