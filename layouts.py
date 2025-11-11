import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🌬️ Качество воздуха", className="main-header")
            ], width=12)
        ], className="header"),


        dbc.Row([
            dbc.Col([
                html.Label("Выберите город:", className='filter-label'),
                dbc.Input(id='city-input', value='Moscow', placeholder="Введите город", type='text', debounce=True, className='filter-label'),
            ], width=4, md=4, xs=12),
            dbc.Col([
               html.Label("Период:", className='filter-label'),
            dbc.RadioItems(
                id='date-selector',
                options=[
                    {'label': '📍 Сегодня', 'value': 'today'},
                    {'label': '📅 Вчера', 'value': 'yesterday'},
                ],
                value='today',  
                inline=True,
                className='radio-items-container')
                ], width=2, md=2, xs=12, className='filter-column'),
            dbc.Col([
               html.Label("Скользящее среднее:", className='moving-average-label'),
            dcc.Checklist(
                id='moving-average',
                options=[{'label': ' Показать скользящее среднее', 'value': True}],
                value=[],
                )
                ], width=2, md=2, xs=12, className='moving-average-container'),
            dbc.Col([
                dbc.Card(id='weather-output', body=True, className='weather-card'),
            ], width=4, md=4, xs=12),
        ], className='filters-row'),

        dbc.Row([
            dbc.Col(dcc.Graph(id='co-graph'), width=4, md=4, xs=12),
            dbc.Col(dcc.Graph(id='no2-graph'), width=4, md=4, xs=12),
            dbc.Col(dcc.Graph(id='o3-graph'), width=4, md=4, xs=12),
        ], className="dash-graph"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='so2-graph'), width=4, md=4, xs=12),
            dbc.Col(dcc.Graph(id='pm2_5-graph'), width=4, md=4, xs=12),
            dbc.Col(dcc.Graph(id='pm10-graph'), width=4, md=4, xs=12),
        ], className="dash-graph")

    ], fluid=True, className="main-container")