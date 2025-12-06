from pico2d import *

import play_mode
from tuar import Tuar
from grass import Grass
import title_mode
import game_world
import game_framework
import store_room
from make_cave import CaveEntrance
from make_wait_bg import Bg
from make_store import Store
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
from gold import gold

cave = None
tuar = None
store = None

def handle_events():
    global cave, tuar
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and cave.overlap:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and  store.overlap:
            game_framework.change_mode(store_room)
        else:
            tuar.handle_event(event)

def init():
    global tuar, cave, tuar, store

    bg = Bg()
    game_world.add_object(bg, 0)

    grass = Grass()
    game_world.add_object(grass, 0)

    store = Store()
    game_world.add_object(store, 0)

    cave = CaveEntrance()
    game_world.add_object(cave, 0)

    tuar = Tuar()
    game_world.add_object(tuar, 1)

    game_world.add_collision_pair('tuar:cave', tuar, cave)
    game_world.add_collision_pair('tuar:store', tuar, store)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    gold.draw(1000, 680)
    update_canvas()

def pause():
    pass

def resume():
    pass