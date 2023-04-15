from pickle import TRUE
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

app.secret_key = "23424fsf"
app.config['SESSION_COOKIE_NAME'] = 'Bridgets cookie' 
TOKEN_INFO = "token info" 

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route('/GetTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iteration = 0
    while TRUE:
        items = sp.current_user_saved_tracks(limit=50, offset= iteration * 50)['items']
        iteration += 1
        all_songs += items
        if (len(items) < 50):
            break
    return str(len(all_songs))

def get_token(): #check if token is expired, if it is then refresh. If there is token data, redirect to login page
    token_info = session.get(TOKEN_INFO, None) #get value from dictionary
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= "968b023ce86f4e9b871853ab40cbbdca",
        client_secret= "9b2bbedb93534859919577076b12a1bd",
        redirect_uri= url_for('redirectPage', _external = True),
        scope= "user-library-read")
    

# "37i9dQZEVXcKmN5d3gTlB2" - ID of Discover Weekly playlist
# "1yolVwqceJD6BfL3tRFTxF" - ID of Saved Weekly playlist

# Get the source and destination playlist IDs
source_playlist_id = "37i9dQZEVXcKmN5d3gTlB2"
destination_playlist_id = "1yolVwqceJD6BfL3tRFTxF"
