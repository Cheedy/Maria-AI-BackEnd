import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

APP_CLIENT_ID = '672f2409c2044d6db771f9c8f3067f59'
APP_CLIENT_SECRET = '1122a7bd99bf4059bda161ec982ed860'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=APP_CLIENT_ID,
                                                           client_secret=APP_CLIENT_SECRET))


name    = 'sch'
q       = f'"{name}" genre:"french hip hop"'
results = spotify.search(q, type='artist', market="FR")

pprint(results['artists']['items'])
