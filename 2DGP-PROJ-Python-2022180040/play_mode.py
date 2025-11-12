from pico2d import *

import draw_ui
import waiting_mode
from tuar2 import Tuar, ROLL_COOLDOWN, SPECIAL_COOLDOWN
import title_mode
from make_dungeon import Dungeon
import game_world
import game_framework

cam_ox, cam_oy = 0, 0
in_ox, in_oy = 0, 0
slide_active = False
slide_t = 0.0
SLIDE_DUR = 0.38
dir_x, dir_y = 0, 0
room_w, room_h = 1024, 720
_pending_spawn = (0, 0)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(waiting_mode)
        else:
            tuar.handle_event(event)

def init():
    global tuar
    global dungeon

    dungeon = Dungeon()
    draw_ui.init()
    tuar = Tuar()

    game_world.add_object(dungeon, 0)
    for w in dungeon.walls:
        game_world.add_object(w, 0)
        game_world.add_collision_pair('tuar:wall', tuar, w)
    for d in dungeon.doors:
        game_world.add_object(d, 0)
        game_world.add_collision_pair('tuar:door', tuar, d)
    game_world.add_object(tuar, 1)


def finish():
    game_world.clear()
    pass


def update():
    global slide_active, slide_t, cam_ox, cam_oy, in_ox, in_oy
    game_world.update()
    game_world.handle_collision()
    if slide_active:
        k = min(1.0, slide_t / SLIDE_DUR)
        cam_ox = -dir_x * room_w * k
        cam_oy = -dir_y * room_h * k
        in_ox = dir_x * room_w * (1.0 - k)
        in_oy = dir_y * room_h * (1.0 - k)

        slide_t += game_framework.frame_time
        if k >= 1.0:
            cam_ox = cam_oy = 0
            in_ox = in_oy = 0
            slide_active = False
            tuar.x, tuar.y = _pending_spawn
    draw_ui.update(_hp=tuar.hp, _hp_max=tuar.max_hp, _roll_cooltime=tuar.roll_cd, _roll_cooltime_max=ROLL_COOLDOWN, _special_cooltime=tuar.special_cd, _special_cooltime_max=SPECIAL_COOLDOWN , _special_active=tuar.special_active)


def draw():
    clear_canvas()
    game_world.render()
    draw_ui.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass

def begin_room_slide(door_name: str, spawn_x: int, spawn_y: int):
    global slide_active, slide_t, dir_x, dir_y, _pending_spawn
    global cam_ox, cam_oy, in_ox, in_oy

    dirmap = {
        'top':    (0,  1),
        'bottom': (0, -1),
        'left':   (-1, 0),
        'right':  (1,  0),
    }
    dx, dy = dirmap.get(door_name, (0, 0))

    slide_active = True
    slide_t = 0.0
    dir_x, dir_y = dx, dy
    _pending_spawn = (spawn_x, spawn_y)

    cam_ox = 0
    cam_oy = 0
    in_ox  = dx * room_w
    in_oy  = dy * room_h
