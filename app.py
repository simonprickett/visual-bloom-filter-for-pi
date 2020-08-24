from flask import Flask
from flask import jsonify
from flask import render_template
import mmh3

API_PATH_PREFIX = 'api'
NUM_HASH_FUNCTIONS = 3
NUM_FILTER_BITS = 64
COLOR_BIT_UNSET = 'TODO'
COLOR_BIT_SET = 'TODO'
COLOR_BIT_QUERY = 'TODO'

app = Flask(__name__)

def add_to_filter(element):
    return True

def exists_in_filter(element):
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
