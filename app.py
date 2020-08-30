from flask import Flask
from flask import jsonify
from flask import render_template
import mmh3
import random # may not be needed long term
import time
import unicornhat

API_PATH_PREFIX = 'api'
NUM_HASH_FUNCTIONS = 3
NUM_LEDS = 64
COLOR_BIT_SET = (255, 0, 0)
COLOR_BIT_WRITING = (255, 165, 0)
COLOR_BIT_QUERYING = (65, 105, 225) 

app = Flask(__name__)

unicornhat.set_layout(unicornhat.AUTO)
unicornhat.rotation(180)
#unicornhat.brightness(0.18)
#unicornhat.brightness(0.19)
unicorn_width, unicorn_height = unicornhat.get_shape()
unicornhat.off()

def get_led_position(led):
    unicorn_width, unicorn_height = unicornhat.get_shape()
    return (led % unicorn_height, led // unicorn_width)

def toggle_led(pos, transition_color, new_color):
    # This should take a list of tuples for all 3 pixels to change...
    # This should also have an interim color to use

    orig_color = unicornhat.get_pixel(pos[0], pos[1])

    for n in range(4):
        unicornhat.set_pixel(pos[0], pos[1], transition_color[0], transition_color[1], transition_color[2])
        unicornhat.show()
        time.sleep(0.3)
        unicornhat.set_pixel(pos[0], pos[1], orig_color[0], orig_color[1], orig_color[2])
        unicornhat.show()
        time.sleep(0.3)

        if n == 3:
            unicornhat.set_pixel(pos[0], pos[1], new_color[0], new_color[1], new_color[2])
            unicornhat.show()

def query_led_status(led):
    pos = get_led_position(led)

    r, g, b = unicornhat.get_pixel(pos[0], pos[1])
    toggle_led(pos, COLOR_BIT_QUERYING, (r, g, b))

    return not (r == 0 and g == 0 and b == 0) 

def set_led_status(led):
    pos = get_led_position(led)
    toggle_led(pos, COLOR_BIT_WRITING, COLOR_BIT_SET)

def add_to_filter(element):
    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS 
        print(str(led))

        set_led_status(led)

    return True

def exists_in_filter(element):
    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS
        print(str(led))
        
        # TODO Test unicorn hat status for this led...
        # If false return false...

        if (query_led_status(led) == False):
            return False

    return True

def reset_filter():
    # TODO animate
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
