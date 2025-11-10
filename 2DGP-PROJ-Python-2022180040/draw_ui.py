from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height
import game_framework
import math

_CW, _CH = 1280, 720

IMG_HP_FILL   = 'image_file/effect/UI/effect_font_0025_life_bar.png'
IMG_HP_FRAME  = 'image_file/effect/UI/effect_font_0024_life_empty.png'
IMG_HP_TEXT   = 'image_file/effect/UI/effect_font_0003_HP.png'
IMG_ICON_TUAR = 'image_file/effect/UI/icon_tuar.png'
IMG_BTN_ROLL  = 'image_file/effect/UI/button_roll.png'
IMG_AWAKEN    = 'image_file/effect/UI/awakening.png'

def init():
    global img_hp_fill, img_hp_frame, img_hp_text
    global img_icon_tuar, img_btn_roll, img_awaken

    img_hp_fill   = load_image(IMG_HP_FILL)
    img_hp_frame  = load_image(IMG_HP_FRAME)
    img_hp_text   = load_image(IMG_HP_TEXT)
    img_icon_tuar = load_image(IMG_ICON_TUAR)
    img_btn_roll  = load_image(IMG_BTN_ROLL)
    img_awaken    = load_image(IMG_AWAKEN)

def update(_hp:int, _hp_max:int, _roll_cooltime:float, _roll_cooltime_max:float,
           _special_cooltime:float, _special_cooltime_max:float, _special_active:bool):
    global hp, hp_max, roll_cooltime, roll_cooltime_max
    global special_cooltime, special_cooltime_max, special_active
    hp = max(0, hp)
    hp_max = max(1, hp_max)
    roll_cooltime = max(0.0, roll_cooltime)
    roll_cooltime_max = max(0.001, roll_cooltime_max)
    special_cooltime = max(0.0, special_cooltime)
    special_cooltime_max = max(0.001, special_cooltime_max)
    special_active = special_active


def draw_hp_bar():
    cw , ch = get_canvas_width(), get_canvas_height()
    x0 = 20
    y0 = ch - 20

    icon_size = 64
    img_icon_tuar.draw(x0 + icon_size // 2, y0 - icon_size // 2, icon_size, icon_size)

    img_hp_text.draw(x0 + icon_size + 10 + 30, y0 - 12, 60, 26)

    frame_w, frame_h = 220, 24
    frame_x = x0 + icon_size + 80
    frame_y = y0 - 12


def draw_skill_icon():
    pass

def main():
    pass

