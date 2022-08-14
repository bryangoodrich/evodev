from gamejam.games.snake.snakebot import agent, population
from gamejam.games.snake import play

savefile = "C:\\Temp\\SnakeSimulationManyHidden.pickle"
ttl = 5000

sim = population.unpickle(savefile)
player = sim[len(sim)-1]['best']
player['ttl'] = ttl
play.lets_play_a_game(player, True)
