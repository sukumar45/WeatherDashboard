import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

df = px.data.gapminder()

app = DjangoDash('SimpleExample2', external_stylesheets=[dbc.themes.BOOTSTRAP])

card_main = dbc.Card(
    [
       
        dbc.CardBody(
            [
                html.H4("Select Location", className="card-title"),
                html.H6("select location:", className="card-subtitle"),
                html.P(
                    "example chart.",
                    className="card-text",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': yr, "value": yr} for yr in df.year.unique()],
                             value=2007, clearable=False, style={"color": "#000000"}),
                # dbc.Button("Press me", color="primary"),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
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

app.layout = html.Div([
    dbc.Row([dbc.Col(card_main, width=3),
             dbc.Col(card_graph1, width=5)], justify="around"),  # justify="start", "center", "end", "between", "around"
    dbc.Row([dbc.Col(card_main, width=3),
             dbc.Col(card_graph2, width=5)], justify="around"),
    
])


@app.callback(
    Output("my_bar1", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = px.scatter(df.query("year=={}".format(str(value))), x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", title=str(value),
                     hover_name="country", log_x=True, size_max=60).update_layout(showlegend=True, title_x=0.5)
    return fig

@app.callback(
    Output("my_bar2", "figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    fig = px.scatter(df.query("year=={}".format(str(value))), x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", title=str(value),
                     hover_name="country", log_x=True, size_max=60).update_layout(showlegend=True, title_x=0.5)
    return fig
