import os
import pandas as pd
import api
from history import alias # no funciona pero está por si acaso

# Leyendo los archivos
filenames = os.listdir('data')
filenames.remove('__pycache__')
history = pd.DataFrame()
for file in filenames:
    part = pd.read_json(open(f'data/{file}', encoding='UTF-8'))
    history = pd.concat([history, part])

# Cambios a columnas y renombrar cosas
history['ts'] = pd.to_datetime(history['ts'])
history = history.set_index(['ts']).sort_index()
# history.index = history.index.tz_localize(None)
# history['spotify_track_uri'] = history['spotify_track_uri'].str[14:]

history.rename(columns=alias['columns'], inplace=True)
history.replace(alias['trackName'], inplace=True)

startdate = '2016-01-01'
enddate = '2030-05-10'
# history = history.loc[startdate : enddate]

# Se crea el song_df
groupby_uri = history.groupby('uri')
_songlist = groupby_uri['trackName'].max()                  # unnecesary
songlist_df = groupby_uri[['trackName', 'albumName', 'artistName']].max()
_m_played = groupby_uri['ms_played'].sum() / 60_000
_play_count = groupby_uri['trackName'].value_counts()

song_df = pd.DataFrame({
    'trackName': _songlist,
    'albumName': songlist_df['albumName'],
    'artistName': songlist_df['artistName'],
    'm_played': _m_played,
    'play_count': _play_count.values},
    index=songlist_df.index
)
# hasta acá cubre la clase History
song_df_full = song_df.sort_values(by=['m_played'], ascending=False)
song_df = song_df_full[:100]
# api.create_song_db(song_df.index)
song_db = pd.read_csv('song_db.csv').set_index('uri')
song_df = pd.concat([song_df, song_db], axis=1)

album_count = history['albumName'].value_counts()
album_playtime = history.groupby('albumName')[
                        'ms_played'].sum().sort_values(ascending=False)/60000
