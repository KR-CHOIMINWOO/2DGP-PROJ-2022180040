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
    hp = max(0, _hp)
    hp_max = max(1, _hp_max)
    roll_cooltime = max(0.0, _roll_cooltime)
    roll_cooltime_max = max(0.001, _roll_cooltime_max)
    special_cooltime = max(0.0, _special_cooltime)
    special_cooltime_max = max(0.001, _special_cooltime_max)
    special_active = _special_active


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

    ratio = min(1.0, max(0.0, hp / float(hp_max)))

    fw, fh = img_hp_fill.w, img_hp_fill.h

    clip_w = int(fw * ratio)
    if clip_w > 0:
        img_hp_fill.clip_draw(0, 0, clip_w, fh, frame_x - frame_w/2 + frame_w*ratio/2, frame_y, frame_w * ratio, frame_h)
    img_hp_frame.draw(frame_x, frame_y, frame_w, frame_h)


def draw_skill_icon():
    cw, ch = get_canvas_width(), get_canvas_height()
    pad = 16
    size = 72

    roll_x = cw - pad - size / 2
    roll_y = pad + size / 2
    special_x = cw - pad * 2 - size * 1.5
    special_y = pad + size / 2

    def draw_with_cd(img, x, y, w, h, cd, cd_max):
        if cd <= 0.0:
            img.opacify(1.0)
            img.draw(x, y, w, h)
        else:
            img.opacify(0.45)
            img.draw(x, y, w, h)
            img.opacify(1.0)

            k = max(0.0, min(1.0, cd / cd_max))

            img.opacify(0.25 + 0.35 * k)
            img.draw(x, y, w, h)
            img.opacify(1.0)


    draw_with_cd(img_btn_roll, roll_x, roll_y, size, size, roll_cooltime, roll_cooltime_max)

    draw_with_cd(img_awaken, special_x, special_y, size, size, special_cooltime, special_cooltime_max)
    if special_active and special_cooltime <= 0.0:
        img_awaken.opacify(0.22)
        img_awaken.draw(special_x, special_y, int(size * 1.06), int(size * 1.06))
        img_awaken.opacify(1.0)

def draw():
    draw_hp_bar()
    draw_skill_icon()

