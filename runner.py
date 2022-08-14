from gamejam.games.snake.snakebot import population


savefile = "C:\\Temp\\SnakeSimulationTanh.pickle"
generations = population.run_simulation(2000, 100)
population.pickle(generations, savefile)

