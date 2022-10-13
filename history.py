import os
import pandas as pd
import api
import yaml
pd.options.mode.chained_assignment = None

PATH = os.path.dirname(__file__)


class History(object):
    """
    Clase que representa el historial de reproducciones de un usuario.
    """

    def __init__(self, call='endsong'):

        with open(os.path.join(PATH, "config.yml")) as ymlfile:
            self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.data = pd.DataFrame()
        self._get_json_data(os.path.join(PATH, "data"), call)
        self.data = self.data[self.data['ms_played'] >= self.config['min_time_ms']]
        self.data = self.data[self.data['incognito_mode'] == False]
        self.data['ts'] = pd.to_datetime(self.data['ts'])
        self.data = self.data.set_index(['ts']).sort_index()
        self.data.rename(columns=self.config['alias']['columns'], inplace=True)
        self.data.replace(self.config['alias']['trackName'], inplace=True)
        self.set_song_df()
        self.top_songs = self.song_df.sort_values(
            by='play_count', ascending=False)[:100]

        self.top_songs = api.complete_song_df(self.top_songs)

    def __repr__(self) -> str:
        return f'''{self.__class__.__name__}(
        Unique songs: {self.songlist.size},
        Attributes: {self.data.shape[1]},
        Entries: {self.data.shape[0]},
        Most recent: {str(self.data.index[-1])})'''

    def _get_json_data(self, path: str, call: str):
        """Obtiene los datos de archivos JSON desde PATH."""
        filenames = [f for f in os.listdir(path) if call in f]
        for file in filenames:
            temp = pd.read_json(open(f'{path}/{file}', encoding='UTF-8'))
            self.data = pd.concat([self.data, temp])

    def replace(self, alias: dict):  # NO SIRVE TODAVÍA
        """Reemplaza los valores de las columnas por los valores de alias. """
        method = dict(
            columns=self.data.rename,
            trackName=self.data.replace
        )
        for key in alias.keys():
            method[key](alias[key], inplace=True)
        self.data.replace(alias, inplace=True)

    def set_song_df(self, columns=None, song_props=None):
        """
        Get song dataframe.
        """
        if columns is None:
            columns = self.config['columns']
        if song_props is None:
            song_props = self.config['song_props']
        self.get_columns()
        song_df = pd.DataFrame({
            'trackName': self.songlist_df['trackName'],
            'albumName': self.songlist_df['albumName'],
            'artistName': self.songlist_df['artistName'],
            'm_played': self.m_played,
            'play_count': self.play_count.values},
            index=self.songlist_df.index
        )
        self.song_df = song_df.sort_values(by='m_played', ascending=False)
        self.song_df = self.song_df[self.song_df['play_count'] > 1]

    def groupby(self, groupby: str):
        """
        Agrupa los datos por una columna.
        """
        return self.data.groupby(groupby)

    def get_columns(self):
        """
        Obtiene una lista de columnas.
        """
        self.groupby_uri = self.data.groupby('uri')
        self.songlist = self.groupby_uri['trackName'].max()
        self.songlist_df = self.groupby_uri[[
            'trackName', 'artistName', 'albumName']].max()
        self.m_played = self.groupby_uri['ms_played'].sum() / 60_000
        self.play_count = self.groupby_uri['trackName'].value_counts()

    def save_from_api(self):
        """
        Obtiene los datos de la API de Spotify.
        """
        song_db = api.create_song_db(self.song_df.index)
        song_db.to_csv('song_db.csv')

    def sort(self, by='m_played', ascending=False, inplace=False):
        """
        Ordena los datos por una columna.
        """
        if inplace:
            self.data.sort_values(by=by, ascending=ascending, inplace=inplace)
        else:
            return self.data.sort_values(by=by, ascending=ascending)

    def export_csv(self, path: str):
        """
        Exporta los datos a un archivo CSV.
        """
        if path == '':
            path = os.path.join(PATH, "data", '2021_11.csv')
        self.data.to_csv(path)

# Faltaría separar el song_df del history y ordenar más cosas de la api y dashapp. Queda!


if __name__ == '__main__':
    H = History()
