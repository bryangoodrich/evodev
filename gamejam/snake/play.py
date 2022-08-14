from gamejam import Conf, pygame
from gamejam.games.snake import assets as Assets, game as Game
from gamejam.games.snake.snakebot import agent as Agent

def get_action(direction, turn=None):
    turns = {
        "UP": (pygame.K_LEFT, pygame.K_RIGHT),
        "LEFT": (pygame.K_DOWN, pygame.K_UP),
        "DOWN": (pygame.K_RIGHT, pygame.K_LEFT),
        "RIGHT": (pygame.K_UP, pygame.K_DOWN)
    }
    return turns[direction][turn] if turn else None

def play(state, snake, apple, agent=None, draw=True):
    while state['paused']:
        Game.menu_scene()
        Game.menu_controller(state)
    
    if draw:
        Game.game_scene()
        Game.print_score(snake['belly'])
        for body in snake['body']:
            Game.draw(body, Game.Color.GREEN)
        Game.draw(apple, Game.Color.RED)
    
    if agent is not None:
        agent['ttl'] -= 1
        agent['steps'] += 1
        agent['score'] = snake['belly']
        if agent['ttl'] <= 0:
            snake['dead'] = True
        sense_data = Agent.look(snake, apple)
        choice = Agent.think(agent, sense_data)
        choice = get_action(snake['direction'], choice)
        action = pygame.event.Event(pygame.KEYDOWN, key=choice)
        if action:
            pygame.event.post(action)
    
    direction = Game.game_controller(state)
    
    snake = Assets.step(snake, direction)
    if Assets.bite(snake, apple):
        snake['belly'] += 1
        snake['length'] += 1
        if agent is not None and 0 < snake['belly'] and snake['belly'] <= 3:
            agent['ttl'] += 100
        apple = Assets.get_valid_apple(snake['body'])
    
    if len(snake['body']) > snake['length']:
        del snake['body'][0]
    
    return state, snake, apple, agent


def game_loop(agent=None):
    clock = pygame.time.Clock()
    fps = Conf['fps']
    state = {
        "gameover": False, 
        "paused": False if agent else True
    }
    while not state['gameover']:
        snake = Assets.get_snake()
        apple = Assets.get_valid_apple(snake['body'])
        while not snake['dead']:
            Game.game_scene()
            state, snake, apple, agent = play(state, snake, apple, agent)
            clock.tick(fps)
        
        state['paused'] = True
        Game.dead_scene(2000)
        while state['paused']:
            Game.menu_scene()
            Game.menu_controller(state)
    
    return agent


def lets_play_a_game(agent=None, create=False):
    pygame.init()
    pygame.font.init()
    pygame.display.set_mode(Conf["window"], pygame.HWSURFACE)
    if create:
        agent = agent if agent is not None else Agent.create_agent()
        game_loop(agent)
    else:
        game_loop()
    pygame.quit()

