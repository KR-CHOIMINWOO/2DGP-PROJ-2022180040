from pico2d import *

from tuar import Tuar
import game_world
import game_framework
import waiting_mode
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
from make_store_bg import Bg
from make_witch import Witch
from store_ui import StoreUI
from gold import gold
tuar = None
bg = None
witch = None
store_ui = None

def handle_events():
    global tuar, witch, store_ui
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if store_ui and store_ui.open:
                store_ui.toggle()
            else:
                game_framework.change_mode(waiting_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and witch.overlap:
            if store_ui:
                store_ui.toggle()
        else:
            if not store_ui or not store_ui.open:
                tuar.handle_event(event)


def init():
    global tuar, bg, witch, store_ui

    bg = Bg()
    game_world.add_object(bg, 0)

    witch = Witch()
    game_world.add_object(witch, 0)

    tuar = Tuar()
    game_world.add_object(tuar, 1)

    game_world.add_collision_pair('tuar:witch', tuar, witch)

    store_ui = StoreUI()

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    gold.draw(850, 680)
    if store_ui:
        store_ui.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass