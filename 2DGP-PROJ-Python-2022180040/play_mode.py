from pico2d import *

import draw_ui
from tuar2 import Tuar, ROLL_COOLDOWN
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

    draw_ui.init()
    tuar = Tuar()
    game_world.add_object(tuar, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    draw_ui.update(_hp=tuar.hp, _hp_max=tuar.max_hp, _roll_cooltime=tuar.roll_cd, _roll_cooltime_max=ROLL_COOLDOWN, _special_cooltime=tuar.special_cd, _special_cooltime_max=15.0, _special_active=tuar.special_active)


def draw():
    clear_canvas()
    game_world.render()
    draw_ui.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass