import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from history import History
import pandas as pd
# 'http://127.0.0.1:8050/'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
min_date = '2016-02-01'
today = lambda: str(pd.Timestamp.today())[:10]

H = History()
song_df = H.song_df
range_str = 'W'
m_played_time = H.data.loc[min_date:].resample(range_str)['ms_played'].sum()/60_000
play_count_time = H.data.loc[min_date:].resample(range_str)['ms_played'].count()

fig = px.line(
    m_played_time,
    x=m_played_time.index,
    y=m_played_time.values,
    labels={'ts': 'Date', 'y': 'Minutes played'}
)

fig2 = px.line(
    play_count_time,
    x=play_count_time.index,
    y=play_count_time.values,
    labels={'ts': 'Date', 'y': 'Amount'}
)

fig3, fig4 = go.Figure(), go.Figure()
sorting_options = dict(ascending=False, ignore_index=True)
songlist_m = song_df.sort_values('m_played', **sorting_options)['trackName']
songlist_c = song_df.sort_values('play_count', **sorting_options)['trackName']

for i in range(20):
    song_streams_m = H.data[H.data['trackName']
                             == songlist_m[i]]
    song_streams_c = H.data[H.data['trackName']
                             == songlist_c[i]]
    song_playtime = song_streams_m['ms_played'].cumsum()/60000
    fig3.add_trace(go.Scatter(
        x=song_playtime.index,
        y=song_playtime.values,
        name=songlist_m[i]
    ))
    fig4.add_trace(go.Scatter(
        x=song_streams_c.index,
        name=songlist_c[i]
    ))

slider_buttons = dict(
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ]
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
fig.update_layout(
    title_text=f'Total minutes played per {range_str}', **slider_buttons)
fig2.update_layout(
    title_text=f'Total songs played per {range_str}', **slider_buttons)
fig3.update_layout(height=800,
                   title_text='Cumulative sum of minutes played per song',
                   **slider_buttons)
fig4.update_layout(height=800,
                   title_text='Song play count',
                   **slider_buttons)

app.layout = html.Div(children=[
    html.H1(children='Spotify History'),

    html.Div(children='''
        Your Spotify Streaming History Analysis
    '''),
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed='2015-01-01',
        max_date_allowed=today(),
        initial_visible_month='2016-02-01',
        end_date=today()
    ),
    dcc.Graph(
        id='minutes-played-time',
        figure=fig
    ),
    dcc.Graph(
        id='play-count-time',
        figure=fig2
    ),
    dcc.Graph(
        id='most-minuted-played-songs',
        figure=fig3
    ),
    dcc.Graph(
        id='song-play-count',
        figure=fig4
    )
])

@app.callback(
    dash.dependencies.Output('minutes-played-time', 'figure'),
    [dash.dependencies.Input('date-range', 'start_date'),
     dash.dependencies.Input('date-range', 'end_date')])
def update_output(start_date, end_date):
    if start_date is not None:
        return fig # start_date
    if end_date is not None:
        return fig # end_date
    else:
        return fig

FIGS = [fig, fig2, fig3, fig4]

if __name__ == '__main__':
    fig.write_html('test.html', include_plotlyjs='cdn', full_html=True)
    fig2.write_html('test2.html', include_plotlyjs=False, full_html=False)
    fig3.write_html('test3.html', include_plotlyjs=False, full_html=False)
    fig4.write_html('test4.html', include_plotlyjs=False, full_html=False)
