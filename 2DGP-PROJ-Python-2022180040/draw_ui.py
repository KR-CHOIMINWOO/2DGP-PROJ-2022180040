from pico2d import load_image, load_font, draw_rectangle
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

def update():
    pass

