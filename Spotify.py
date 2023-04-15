from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask('name')

app.secret_key = "23424fsf"
app.config['SESSION_COOKIE_NAME'] = 'Bridgets cookie' 

@app.route('/')
def index():
    return 'Bridgets home page'

@app.route('/GetTracks')
def getTracks():
    return 'some Drake songs'

