import matplotlib.pyplot as plt
import numpy as np
from history import History

H = History()
history = H.data
startdate = history.index[0]
enddate = history.index[-1]
song_df = H.song_df
# album_playtime = H.album_playtime

def plot_m_played_total(start=startdate, end=enddate, interval='2W'):
    date_playtime = history.loc[start:end].resample(
        interval)['ms_played'].sum()/60000
    plt.figure(figsize=(24, 6))
    plt.plot(date_playtime.index, date_playtime.values)
    plt.tight_layout()
    plt.show()


def plot_play_count_total(start=startdate, end=enddate, interval='2W'):
    date_count = history.loc[start:end].resample(interval)['ms_played'].count()
    plt.figure(figsize=(24, 6))
    plt.plot(date_count.index, date_count.values)
    plt.tight_layout()
    plt.show()


def plot_m_played():
    plt.figure(figsize=(24, 6))
    for i in range(20):
        songname = song_df['trackName'][i]
        song_date_count = history[history['trackName']
                                  == songname]['ms_played'].cumsum()/60000
        plt.plot(song_date_count.index, song_date_count.values, label=songname)
    plt.legend(loc='upper left', framealpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_album_playtime():
    plt.figure(figsize=(24, 6))
    for i in range(20):
        albumname = album_playtime.index[i]
        album_date_count = history[history['albumName']
                                   == albumname]['ms_played'].cumsum()/60000
        plt.plot(album_date_count.index,
                 album_date_count.values, label=albumname)
    plt.legend(loc='upper left', framealpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_play_count():
    plt.figure(figsize=(24, 6))
    for i in range(20):
        songname = song_df['trackName'][i]
        song_dates = history[history['trackName']
                             == songname].index
        plt.plot(song_dates, np.arange(
            1, song_dates.size+1, 1), label=songname)
    plt.legend(loc='upper left', framealpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    breakpoint()