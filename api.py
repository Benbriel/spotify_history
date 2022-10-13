import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

try:
    import credentials
except ImportError:
    print('No credentials.py file found. Please create one with your Spotify credentials "cid", "secret" and "username".')
    exit()

cid = credentials.cid
secret = credentials.secret
username = credentials.username

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

default_columns = ['duration_ms', 'time_signature', 'key', 'tempo',
                       'danceability', 'energy', 'loudness', 'mode',
                       'speechiness', 'acousticness', 'instrumentalness',
                       'liveness', 'valence']

def search_uri(df, song_df):
    song_uri = []
    for song in song_df.index:
        artist = df['artistName'][df['trackName'] == song][0]
        try:
            song_uri.append(sp.search(q='track:' + song + ' artist:' + artist,
                            type='track', limit=1,
                            market='CL')['tracks']['items'][0]['uri'])
        except:
            song_uri.append(None)
    return song_uri


def create_song_db(uri_list, columns=None):
    song_db = pd.DataFrame(index=uri_list)
    song_audio_features = pd.DataFrame(sp.audio_features(
        tracks=uri_list),
        index=uri_list)

    if columns is None:
        columns = default_columns
    song_db[columns] = song_audio_features[columns]

    return song_db


def complete_song_df(song_df, columns=None):
    song_audio_features = pd.DataFrame(sp.audio_features(
        tracks=song_df.index),
        index=song_df.index)

    if columns is None:
        columns = default_columns
    song_df[columns] = song_audio_features[columns]
    
    song_df['retain'] = song_df['m_played']*60000 / \
        (song_df['play_count']*song_df['duration_ms'])

    return song_df
