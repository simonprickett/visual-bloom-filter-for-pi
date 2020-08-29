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
COLOR_BIT_UNSET = 'TODO'
COLOR_BIT_SET = 'TODO'
COLOR_BIT_QUERY = 'TODO'

app = Flask(__name__)

unicornhat.set_layout(unicornhat.AUTO)
unicornhat.rotation(180)
unicornhat.brightness(0.18)
unicorn_width, unicorn_height = unicornhat.get_shape()
unicornhat.off()

for y in range(unicorn_height):
    for x in range(unicorn_width):
       unicornhat.set_pixel(x, y, random.randrange(50, 255), random.randrange(50, 255), random.randrange(50, 255))
       unicornhat.show()
       time.sleep(0.2)


def add_to_filter(element):
    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS 
        print(str(led))

    return True

def exists_in_filter(element):
    for n in range(NUM_HASH_FUNCTIONS): 
        led = mmh3.hash(element, n) % NUM_LEDS
        print(str(led))
        
        # TODO Test unicorn hat status for this led...
        # If false return false...

    return True

def reset_filter():
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
