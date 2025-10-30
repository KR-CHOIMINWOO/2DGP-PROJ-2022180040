from pico2d import *
from tuar import Tuar
from grass import Grass
import title_mode
import game_world
import game_framework

def handle_events():

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            tuar.handle_event(event)

def init():
    global tuar

    grass = Grass()
    game_world.add_object(grass, 0)

    tuar = Tuar()
    game_world.add_object(tuar, 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass