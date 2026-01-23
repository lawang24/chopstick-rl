from enum import Enum
from typing import Literal, TypeAlias

class Actions(Enum):
    tap = 'tap'
    split = 'split'

ActionType = Literal[Actions.tap, Actions.split]
Move: TypeAlias = tuple[ActionType, tuple[int, int]]
GamePosition: TypeAlias = tuple[tuple[int, int], tuple[int, int]]