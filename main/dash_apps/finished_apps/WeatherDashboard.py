import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
###
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px


# PRE-PROCESSING
location_data = pd.read_csv("/data/locationData.csv") #Check the path (different for Linux and Windows)
location_map = pd.read_csv("/data/locationMap.csv")
location_data = location_data.drop(labels=0, axis=0)
features = ['WindDirection', 'WindSpeed', 'Gust' ]
location_data[features] = location_data[features].fillna(0)
location_data['AtmosphericPressure'] = location_data['AtmosphericPressure'].astype(float)
location_data['WindDirection'] = location_data['WindDirection'].astype(float)
location_data['WindSpeed'] = location_data['WindSpeed'].astype(float)
location_data['Gust'] = location_data['Gust'].astype(float)
pressure_mean_value = location_data['AtmosphericPressure'].dropna().sum()/location_data['AtmosphericPressure'].dropna().shape[0]
location_data['AtmosphericPressure'] = location_data['AtmosphericPressure'].fillna(pressure_mean_value)

df1 = location_data['locationID'].unique()
df1 = df1.tolist()
app = DjangoDash('WeatherDashboard', external_stylesheets=[dbc.themes.SOLAR])

# DASHBOARD ELEMENTS
card_main = dbc.Card(
    [
        
        dbc.CardBody(
            [
                html.H4("Select Location", className="card-title"),
                html.H6("M1 -- Kinsale ", className="card-subtitle"),
                html.H6("M2 -- Crosshaven ", className="card-subtitle"),
                html.H6("M3 -- Cobh ", className="card-subtitle"),
                html.H6("M4-Archive -- Skibbereen ", className="card-subtitle"),
                html.H6("M4 -- Skibbereen (latest) ", className="card-subtitle"),
                html.H6("M5 -- Bantry ", className="card-subtitle"),
                html.H6("M6 -- Ballydebhob ", className="card-subtitle"),
                html.H6("FS1 -- Youghal ", className="card-subtitle"),
                html.H6("Belmullet-AMETS -- Roscarbery ", className="card-subtitle"),
                html.P(
                    "Choose one location from the dropdown",
                    className="card-text",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': loc_id, "value": loc_id} for loc_id in df1],
                             value='M1', clearable=False, style={"color": "#000000"}),
                
            ]
        ),
    ],
    color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)



card_graph1 = dbc.Card(
        dcc.Graph(id='my_bar1', figure={}), body=True, color="secondary",
)
card_graph2 = dbc.Card(
        dcc.Graph(id='my_bar2', figure={}), body=True, color="secondary",
)
card_graph3 = dbc.Card(
        dcc.Graph(id='my_bar3', figure={}), body=True, color="secondary",
)


app.layout = html.Div([
    dbc.Row([dbc.Col(card_main, width=5),
             dbc.Col(card_graph1, width=5)], justify="center"),  # justify="start", "center", "end", "between", "around"
    dbc.Row([dbc.Col(card_graph2, width=5), 
             dbc.Col(card_graph3, width=5)], justify="center"),
    
])

def wind_news(df):
        df = df[df['WindDirection'] > 0]
        df['WindDirection'][ df['WindDirection'] < 11.25 ] = df['WindDirection'][ df['WindDirection'] < 11.25 ].apply(lambda x : x+360)
    
        wind_df = pd.DataFrame(columns=['direction', 'speed', 'frequency'])
        angle = [ (i * 22.5 - 11.25 + 360) % 360.0 for i in range(16) ]
        direction = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        speed = [i*2.5 for i in range(1, 9)]
        tot = 0
        for ang, d  in zip(angle, direction):
            for s in speed:
                cnt = df[(ang <= df['WindDirection'] ) & ( df['WindDirection'] < ang+22.5 )&  (s-2.5 <= df['WindSpeed']) & (df['WindSpeed'] < s) ].shape[0]
                tot += cnt
                wind_df = wind_df.append({'direction': d, 'speed':s, 'frequency': cnt }, ignore_index=True)
        return wind_df 

def wind_direction_plot(df):
    wind = wind_news(df)
    fig = px.bar_polar(wind, r="frequency", theta="direction",
                    color="speed", template="plotly_dark",
                    color_discrete_sequence= px.colors.sequential.Plasma[-2::-1])
    fig = fig.update_layout(title_text='Wind Direction')
    
    return fig

def wind_graph(df):
    df = df.sort_values('time')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['WindSpeed'], name="Wind Speed", line_color='royalblue', opacity=0.7))
    fig =fig.update_layout(template='plotly_dark',title_text='Wind Speed', xaxis_rangeslider_visible=True)
    return fig

def pressure_graph(df):
    df = df.sort_values('time')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['AtmosphericPressure'], name="Atmospheric Pressure", line_color='#1bbfbd', opacity=0.7))
    fig = fig.update_layout(template='plotly_dark',title_text='Atmospheric Pressure', xaxis_rangeslider_visible=True)
    return fig

#CALLBACKS WITH ACTIONS
@app.callback(
    Output("my_bar1", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = wind_direction_plot(location_data[location_data['locationID'] == value])
    return fig
   

@app.callback(
    Output("my_bar2", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = wind_graph(location_data[location_data['locationID'] == value])
    return fig

@app.callback(
    Output("my_bar3", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = pressure_graph(location_data[location_data['locationID'] == value])
    return fig
