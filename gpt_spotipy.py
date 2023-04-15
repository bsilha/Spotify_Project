##Author: Bridget Silha

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

# saving client ID in session so that user stays logged in
app.config['SESSION_COOKIE_NAME'] = 'Bridgets cookie'
app.secret_key = "23424fsf"  # secure digital signature for session
TOKEN_INFO = "token info"

# Route 1: Home route
app.route('/')
def login():
    # getting an authorized url from Spotify
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)  # redirect user to authorized url


# Route 2: Redirect route
app.route('/redirect')
def redirect_page():
    session.clear()  # clears any existing user data
    # pulls code request and stored in 'code' variable
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)  # exchanges auth code for an access token
    session[TOKEN_INFO] = token_info  # store token info in session
    return redirect(url_for('save_discover_weekly', _external=True))


# Route 3: Saved Discover Weekly route
app.route('/savediscoverweekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/")
    
    return ("OAUTH SUCCESSFUL")


def get_token():  # create function to get token
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:  # if token doesn't exist, redirect user back to login page
        redirect(url_for('login', _external=False))

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oath = create_spotify_oauth()
        token_info = spotify_oath.refresh_access_token(token_info['refresh token'])
        return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='968b023ce86f4e9b871853ab40cbbdca',
        client_secret='9b2bbedb93534859919577076b12a1bd',
        redirect_uri=url_for(('redirect_page'), _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug= True)


# Get all playlists
# Find playlist ID for "Saved Weekly"
# If playlist does not exist, create "Saved Weekly" playlist
# Get all Track URIs from Discover Weekly and save into a list
# Save tracks to new playlist
