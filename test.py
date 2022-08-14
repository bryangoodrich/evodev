from gamejam.games.snake.snakebot import genome as Genome
from gamejam.games.snake.snakebot import graph as Graph
from functools import reduce

genome = Genome.random_genome(100)
g = Graph.create(genome)
for gene in genome: 
    print(gene)
print("")
paths = [Graph.dfs(g, sense) for sense in Genome.SenseLayer]
for sense in paths:
    for path in sense:
        s = reduce(lambda x, y: f"{x} -> {y}", path)
        print(s)

