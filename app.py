from flask import Flask
from flask import render_template
import mmh3

API_PATH_PREFIX = 'api'

app = Flask(__name__)

@app.route(f'/{API_PATH_PREFIX}/add/<element>')
def add(element):
    return f'TODO: ADD {element}'

@app.route(f'/{API_PATH_PREFIX}/exists/<element>')
def exists(element):
    return f'TODO: EXISTS {element}'

@app.route('/')
def homepage():
    return render_template('homepage.html')
