import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import api

filenames = os.listdir('data_streaming')
filenames.remove('__pycache__')

history = pd.DataFrame()
for file in filenames:
    part = pd.read_json(open(f'data_streaming/{file}', encoding='UTF-8'))
    history = pd.concat([history, part])

history = history.rename(
    columns={
        'msPlayed': 'ms_played',
        'endTime':'ts'})

history['ts'] = pd.to_datetime(history['ts'])
history = history.set_index(['ts']).sort_index()
history.index = pd.to_datetime(history.index)

songlist = history['trackName'].unique()

song_count = history['trackName'].value_counts()
song_playtime = history.groupby('trackName')[
    'ms_played'].sum().sort_values(ascending=False)/60000

song_df = pd.DataFrame({'song_playtime': song_playtime,
                       'song_count': song_count}).dropna()
song_df = song_df.sort_values(by=['song_playtime'], ascending=False)[:100]

