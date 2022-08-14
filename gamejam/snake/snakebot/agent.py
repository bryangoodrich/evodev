import itertools
import uuid
from functools import reduce

import numpy as np
from gamejam import Conf
from gamejam.games.snake import game as Game


def create_brain(weights=None, layers=(24, 16, 16, 3)):
    w = weights if weights is not None else randomweights2(layers)
    return {
        "layers": layers,
        "weights": w
    }


def activation(x, method="relu"):
    methods = {
        "relu": lambda x: x * (x > 0),
        "leaky": lambda x, ns=1e-2: (x * (x > 0)) + (ns * x * (x <= 0)),
        "sigmoid": lambda x: 1 / (1 + np.exp(-x)),
        "tanh": np.tanh
    }
    return methods[method](x)


def randomweights(size):
    index = range(len(size)-1)
    return [2*np.random.rand(size[i], size[i+1])-1 for i in index]


def randomweights2(size, lwr=-2**15, upr=2**15):
    index = range(len(size)-1)
    return [np.random.randint(lwr, upr, (size[i], size[i+1])) / 2**14 for i in index]


def feedforward(nnet, data, afun="relu"):
    return reduce(lambda i, a: activation(np.dot(i, a), afun), nnet['weights'], data)


def create_agent(brain=None, ttl=200):
    agent = {
        "id": uuid.uuid4(),
        "brain": create_brain() if brain is None else brain,
        "fitness": 0,
        "score": 0,
        "steps": 0,
        "ttl": ttl
    }
    return agent


def clone(agent):
    mrsmith = create_agent(agent['brain'])
    mrsmith['id'] = agent['id']
    return mrsmith


def steps():
    gz = Conf['cellsize']
    directions = [(-gz, 0), (0, -gz), (gz, 0), (0, gz), 
        (-gz, -gz), (gz, -gz), (-gz, gz), (gz, gz)]
    return directions


def compute_fitness(agent):
    s = agent['steps']
    score = agent['score']
    return int((s**2 * score**2)/100) if (score < 10) else (s**2 * (score-9))


def distance(step, head, apple, tail, wall):
    pos = head.move(0,0)
    distance = {"to_apple": 0, "to_tail": 0, "to_wall": 0}
    found = {"apple": False, "tail": False}
    d = 0
    while wall.contains(pos):
        pos = pos.move(step)
        d += 1
        if not found['tail'] and pos.collidelistall(tail):
            distance['to_tail'] = 1
            found['tail'] = True
        
        if not found['apple'] and pos.colliderect(apple):
            distance['to_apple'] = 1 
            found['apple'] = True
    
    distance['to_wall'] = 1 / d
    return list(distance.values())


# 4-way keypad choice (obsolete)
# def choose(opt):
#     keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
#     return keys[opt.argmax(axis=0)]

# def choose(opt):
#     idx = abs(opt).argmax(axis=0)
#     activated = abs(opt[idx]) > 0.5
#     return idx if activated else None
    

def choose(opt):
    idx = abs(opt).argmax(axis=0)
    return None if idx==2 else idx


def think(agent, sensor):
    result = feedforward(agent['brain'], sensor, afun="sigmoid")
    return choose(result)


def look(snake, apple):
    wall = Game.window()
    head = snake['body'][-1]
    tail = snake['body'][:-1]
    distances = [distance(step, head, apple, tail, wall) for step in steps()]
    return tuple(itertools.chain(*distances))
