from utils.data_loader import load_data
import plotly.graph_objects as go
from dash import Input, Output, html
from datetime import date,  timedelta
import pandas as pd
from assets.design import GRAPH_FONT_FAMILY, GRAPH_FONT_SIZE

def register_callbacks(app):
    
    @app.callback(
            [Output('weather-output', 'children'),
            Output('co-graph', 'figure'),
            Output('no2-graph', 'figure'),
            Output('o3-graph', 'figure'),
            Output('so2-graph', 'figure'),
            Output('pm2_5-graph', 'figure'),
            Output('pm10-graph', 'figure')],
            [Input('city-input', 'value'),
            Input('date-selector', 'value')],
            Input('moving-average', 'value')
    )


    def update_dashboard(city,date_period='today', moving_average_enabled=None):

        if moving_average_enabled is None:
            moving_average_enabled = False
        elif isinstance(moving_average_enabled, list):
            moving_average_enabled = bool(moving_average_enabled)
        
        if date_period == 'today':
            selected_date = date.today().isoformat()
            date_display = "сегодня"
        elif date_period == 'yesterday':
            selected_date = (date.today() - timedelta(days=1)).isoformat()
            date_display = "вчера"
        else:
            selected_date = date.today().isoformat()
            date_display = "сегодня"

        data = load_data(city, selected_date)

        def create_figure(x_data, y_data, title, y_title, window_size=5):
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                name='Фактические значения',
                line=dict(color='#1f77b4')
            ))

            if moving_average_enabled and len(y_data)>= window_size:
                series = pd.Series(y_data)
                moving_avg = series.rolling(window = window_size, center=True).mean()
                fig.add_trace(go.Scatter(
                    x=x_data, 
                    y=moving_avg, 
                    mode='lines',
                    name=f'Скользящее среднее (окно = {window_size})',
                    line=dict(color='#ff7f0e', width=3, dash='dash')
                ))

            fig.update_layout(
                    title=title, 
                    xaxis_title='Время', 
                    yaxis_title=y_title,
                    template='plotly_dark',
                    showlegend=moving_average_enabled 
            )
            return fig 
        
        co_fig = create_figure(
            data['hours'], data['co'], 
            "Концентрация угарного газа по часам", 
            "Концентрация CO (µg/m³)"
        )

        no2_fig = create_figure(
            data['hours'], data['no2'], 
            "Концентрация диоксида азота по часам", 
            "Концентрация NO2 (µg/m³)"
        )

        o3_fig = create_figure(
            data['hours'], data['o3'], 
            "Концентрация озона по часам", 
            "Концентрация O3 (µg/m³)"
        )  

        so2_fig = create_figure(
            data['hours'], data['so2'], 
            "Концентрация сернистого газа по часам", 
            "Концентрация SO2 (µg/m³)"
        )

        pm2_5_fig = create_figure(
            data['hours'], data['pm2_5'], 
            "Концентрация мелкодисперсных частиц по часам", 
            "Концентрация %"
        )

        pm10_fig = create_figure(
            data['hours'], data['pm10'], 
            "Концентрация грубых частиц по часам", 
            "Концентрация %"
        )

        weather_output = html.Div([
            html.H4(f"{data['city_name']}", style={'margin-bottom': '10px', 
            'color': '#e0e0e0',
            'fontFamily': GRAPH_FONT_FAMILY,
            'fontSize': GRAPH_FONT_SIZE} ),
            html.P(f"Дата: {selected_date}", style={'margin': '0', 'fontSize': '14px', 'color': '#e0e0e0', }),
            html.Img(src=f"https:{data['icon']}", style={'width': '64px', 'height': '64px'}),
            html.H5(f"{data['temp']} C", style={'margin': '0', 'fontFamily': GRAPH_FONT_FAMILY, 'color': '#e0e0e0', 'fontSize': '28px'}),
            html.P(f"{data['condition']}", style={'margin': '0', 'fontSize': '14px'})
        ]
        )
        return weather_output, co_fig, no2_fig, o3_fig, so2_fig, pm2_5_fig, pm10_fig
