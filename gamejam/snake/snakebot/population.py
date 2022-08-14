# Useful resource
# https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_quick_guide.htm

import json
import pickle as pk
import random
import time

import numpy as np
from gamejam import Conf, pygame
from gamejam.games.snake import assets as Assets, play as Play
from gamejam.games.snake.snakebot import agent as Agent


def create_population(agents=None, generation=1, best=None, n=2000):
    """ Crate a Population type """
    if agents is None:
        agents = [Agent.create_agent() for _ in range(n)]
    
    population = {
        "generation": generation,
        "agents": agents,
        "fitness": [agent['fitness'] for agent in agents],
        "best": best
    }
    return population


def select_mates(population):
    return random.choices(population['agents'], population['fitness'], k=2)


def selection(population):
    """ Proportionate Selection """
    n = len(population['agents'])-1
    while n > 0:
        mates = select_mates(population)
        if mates[0]['id'] != mates[1]['id']:
            yield mates
            n = n-1


def crossover(parents, mr=0.05):
    brain1, brain2 = [parent['brain']['weights'] for parent in parents]
    layers = parents[0]['brain']['layers']
    N = len(brain1)
    weights = [None]*N
    for n in range(N):
        shape = brain1[n].shape
        r = np.random.rand(*shape) < 0.5
        mutation = np.random.rand(*shape) < mr
        bias = (np.random.normal(size=shape)/5) * mutation
        w = brain1[n]*r + brain2[n]*np.invert(r)
        weights[n] = np.clip(w+bias, -1, 1)
    return Agent.create_brain(weights, layers)


def crossover2(parents, mr=0.05):
    brain1, brain2 = [parent['brain']['weights'] for parent in parents]
    layers = parents[0]['brain']['layers']    
    N = len(brain1)
    weights = [None]*N
    for n in range(N):
        shape = brain1[n].shape
        mutation = np.random.rand(*shape) < mr
        bias = (np.random.normal(size=shape)/5) * mutation
        r = np.random.randint(np.prod(shape))
        p = (brain1[n].flatten()[:r], brain2[n].flatten()[r:])
        w = np.concatenate(p).reshape(shape)
        weights[n] = np.clip(w+bias, -1, 1)
    return Agent.create_brain(weights, layers)


def reproduction(parents, mr):
    brain = crossover(parents, mr)
    return Agent.create_agent(brain)


def get_fitness(agents):
    return [agent['fitness'] for agent in agents]


def select_best(agents):
    return agents[np.argmax([agent['score'] for agent in agents])]


def natural_selection(population, mr=0.05):
    population['fitness'] = get_fitness(population['agents'])
    best = select_best(population['agents'])
    population['best'] = best
    babies = [
        reproduction(parents, mr)
        for parents in selection(population)
    ]
    babies.append(Agent.clone(best))
    return create_population(babies, population['generation']+1, None)


def game_loop(agent):
    state = {"gameover": False, "paused": False}
    snake = Assets.get_snake()
    apple = Assets.get_valid_apple(snake['body'])
    while not snake['dead']:
        state, snake, apple, agent = Play.play(state, snake, apple, agent, False)

    agent['fitness'] = Agent.compute_fitness(agent)
    return agent


def simulation(population):
    population['agents'] = [game_loop(agent) for agent in population['agents']]
    return population


def run_simulation(n=2000, generations=30):
    try:
        pygame.init()
        pygame.display.set_mode(Conf['window'], pygame.HWSURFACE)
        generation = [None]*(generations+1)
        babies = [Agent.create_agent() for _ in range(n)]
        generation[0] = create_population(babies)
        for i in range(generations):
            tic = time.time()
            population = simulation(generation[i])
            zeros = len([a for a in population['agents'] if a['score'] == 0])
            generation[i+1] = natural_selection(population)
            toc = time.time()
            print(f"Completed generation {i+1} in {abs(tic-toc):.0f} seconds; total fitness {sum(population['fitness'])}. Best snake score {population['best']['score']}. {zeros} zeros")
        return generation[:-1]
    finally:
        pygame.quit()


def save(obj, path):
    with open(path, 'w') as fh:
        json.dump(obj, fh)


def pickle(obj, path):
    with open(path, 'wb') as fh:
        pk.dump(obj, fh)


def load(path):
    with open(path, 'r') as fh:
        data = json.load(fh)
    return data


def unpickle(path):
    with open(path, 'rb') as fh:
        obj = pk.load(fh)
    return obj
