from typing import TypedDict, Tuple, List, NewType
from numpy.typing import ArrayLike
from uuid import UUID
from pygame import Rect


NNetLayers = NewType("NNetLayers", Tuple[int])
NNetWeights = NewType("NNetWeights", List[ArrayLike])
PositiveInt = NewType("PositiveInt", int)
NonNegativeInt = NewType("NonNegativeInt", int)
MutationRate = NewType("MutationRate", float)
Direction = NewType("Direction", str)
Coordinates = NewType("Coordinates", Tuple[int, int])
Apple = NewType("Apple", Rect)


class Brain(TypedDict):
    layer: NNetLayers
    weights: NNetWeights


class Agent(TypedDict):
    id: UUID
    brain: Brain
    fitness: NonNegativeInt
    score: NonNegativeInt
    steps: NonNegativeInt
    ttl: NonNegativeInt


Agents = NewType("Agents", List[Agent])
Parents = NewType("Parents", Tuple[Agent])


class Population(TypedDict):
    generation: PositiveInt
    agents: Agents
    fitness: List[NonNegativeInt] # maybe be come part of a population stats type?
    best: Agent


SnakeBody = NewType("SnakeBody", List[Rect])

class Snake(TypedDict):
    dead: bool
    length: PositiveInt
    belly: NonNegativeInt
    body: SnakeBody
    direction: Direction # should proably be an enum


