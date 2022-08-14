# useful resource: https://algs4.cs.princeton.edu/40graphs/
import random
from dataclasses import dataclass
from enum import Enum

import numpy as np
from gamejam.games.snake.snakebot import graph as Graph


class SenseLayer(Enum):
    xcoord=1
    ycoord=2
    toapple=3


class ActionLayer(Enum):
    turnleft=1
    turnright=2


class HiddenLayer(Enum):
    H1=1
    H2=2
    H3=3
    H4=4

@dataclass(frozen=True)
class Gene:
    left: Enum
    right: Enum
    weight: float
    
    def __str__(self):
        return f"{self.left} -> {self.right} ({self.weight:0.4f})"


def random_gene():
    sense = random.getrandbits(1)
    action = random.getrandbits(1)
    source = random.choice(list(SenseLayer) if sense else list(HiddenLayer))
    sink = random.choice(list(ActionLayer) if action else list(HiddenLayer))
    weight = np.random.uniform(-1, 1)
    return Gene(left=source, right=sink, weight=weight)


def _random_genome(n=16):
    count = n
    while count > 0:
        gene = random_gene()
        if gene.left != gene.right:
            yield gene
            count = count - 1


def random_genome(n=16):
    return list(_random_genome(n))





def activate(g, x, v, func=np.tanh):
    perceptron = {}
    for w in g.adj[v]:
        val = func(x*w.weight)
        perceptron.setdefault(w.right, []).append(val)
    return perceptron


