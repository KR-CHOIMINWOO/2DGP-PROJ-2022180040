from pico2d import *
import game_framework
import game_world
import title_mode

image = None
logo_start_time = 0.0

def init():
    global image, logo_start_time

    image = load_image('tuk_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image #like free from C/C++

def update():
    global logo_start_time

    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    event_list = get_events() #버퍼로부터 모든 입력을 갖고 온다.
    # no nothing
    #로고가 올라오는 중에 키를 눌러도 아무 반응이 없도록 한다.

def pause():
    pass

def resume():
    pass