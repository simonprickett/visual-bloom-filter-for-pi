from flask import Flask
from flask import jsonify
from flask import render_template
import mmh3
import random # may not be needed long term
import time
import unicornhat

API_PATH_PREFIX = 'api'
NUM_HASH_FUNCTIONS = 3
COLOR_BIT_SET = (255, 0, 0)
COLOR_BIT_WRITING = (0, 255, 0)
COLOR_BIT_QUERYING = (0, 0, 255) 
NUM_TRANSITIONS = 4

app = Flask(__name__)

unicornhat.set_layout(unicornhat.AUTO)
unicornhat.rotation(180)
unicornhat.brightness(0.19)
unicorn_width, unicorn_height = unicornhat.get_shape()
unicornhat.off()

NUM_LEDS = unicorn_width * unicorn_height

def get_led_position(led):
    unicorn_width, unicorn_height = unicornhat.get_shape()
    return (led % unicorn_height, led // unicorn_width)

def toggle_leds(leds, transition_color, new_color):
    orig_colors = []

    for led in leds: 
        orig_colors.append(unicornhat.get_pixel(led[0], led[1]))

    for n in range(NUM_TRANSITIONS):
        for l in range(len(leds)):
            this_led = leds[l]
            unicornhat.set_pixel(this_led[0], this_led[1], transition_color[0], transition_color[1], transition_color[2])
        unicornhat.show()
        time.sleep(0.3)
       
        for l in range(len(leds)): 
            this_led = leds[l]
            this_orig_color = orig_colors[l]
            unicornhat.set_pixel(this_led[0], this_led[1], this_orig_color[0], this_orig_color[1], this_orig_color[2])
        unicornhat.show()
        time.sleep(0.3)

        if n == (NUM_TRANSITIONS - 1):
            for l in range(len(leds)):
                this_led = leds[l]
                unicornhat.set_pixel(this_led[0], this_led[1], new_color[0], new_color[1], new_color[2])
                unicornhat.show()

def query_led_status(led):
    pos = get_led_position(led)

    r, g, b = unicornhat.get_pixel(pos[0], pos[1])
    toggle_leds([pos], COLOR_BIT_QUERYING, (r, g, b))

    return not (r == 0 and g == 0 and b == 0) 

def set_led_status(leds):
    led_positions = []

    for led in leds:
        led_positions.append(get_led_position(led))

    toggle_leds(led_positions, COLOR_BIT_WRITING, COLOR_BIT_SET)

def add_to_filter(element):
    leds = []

    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS 
        print(str(led))

        leds.append(led)

    set_led_status(leds)
    return True

def exists_in_filter(element):
    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS
        print(str(led))

        if (query_led_status(led) == False):
            return False

    return True

def reset_filter():
    for n in range(2):
        unicornhat.set_all(0, 0, 255)
        unicornhat.show()
        time.sleep(0.3)
        unicornhat.off()
        time.sleep(0.3)

    unicornhat.off()
    return True

@app.route(f'/{API_PATH_PREFIX}/add/<element>', methods=['POST'])
def add(element):
    return jsonify({ 'result': add_to_filter(element) }), 201

@app.route(f'/{API_PATH_PREFIX}/exists/<element>')
def exists(element):
    return jsonify({ 'result': exists_in_filter(element) })

@app.route(f'/{API_PATH_PREFIX}/reset', methods=['POST'])
def reset():
    return jsonify({ 'result': reset_filter() })

@app.route('/')
def homepage():
    return render_template('homepage.html')
