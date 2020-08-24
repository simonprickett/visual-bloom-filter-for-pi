from flask import Flask
from flask import render_template
import mmh3

API_PATH_PREFIX = 'api'
NUM_HASH_FUNCTIONS = 3
NUM_FILTER_BITS = 64

app = Flask(__name__)

@app.route(f'/{API_PATH_PREFIX}/add/<element>')
def add(element):
    return f'TODO: ADD {element}'

@app.route(f'/{API_PATH_PREFIX}/exists/<element>')
def exists(element):
    return f'TODO: EXISTS {element}'

@app.route(f'/${API_PATH_PREFIX}/reset')
def reset():
    return 'TODO: RESET'

@app.route('/')
def homepage():
    return render_template('homepage.html')
