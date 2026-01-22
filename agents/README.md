# Agents

This directory contains implementations of various agents (human, random, neural network) that interact with the Game API to make moves.

## Overview

All agents follow a consistent interface and interact with the game through a standardized API. All unique types are defined in `custom_types.py`.

## Game Position Format

`GamePosition` is defined as:
```python
[[p1_hand1, p1_hand2], [p2_hand1, p2_hand2]]
```

**Note:** We always consider `p1` as the current player's move.

## Game API

The `Game` class provides the following interface:

```python
class Game:
    def get_state(self) -> GamePosition:
        """Returns the current game position."""
        pass
    
    def make_move(self, move: Move) -> GamePosition:
        """Makes a move and returns the new game position."""
        pass
    
    def is_over(self) -> bool:
        """Returns True if the game is over."""
        pass
```

## Agent Interface

All agents must implement the following interface:

```python
class Agent:
    def get_move(self, position: GamePosition) -> Move:
        """Generates a move given a GamePosition."""
        pass
```

## Example Usage

Here's an example of how to run a two-player game:

```python
agent1 = Agent()
agent2 = Agent()
game = Game()

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
```
