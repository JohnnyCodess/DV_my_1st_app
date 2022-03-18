import plotly.graph_objects as go
import pandas as pd
import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df=pd.read_csv('df_preprocessed.csv')
print(df.head())

# Requirements for the dash core components

crypto_options = [{'label': 'Bitcoin!', 'value': 'Bitcoin'},
           {'label': 'Ethereum!', 'value': 'Ethereum'},
           {'label': 'Dogecoin!', 'value': 'Dogecoin'}]

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('Título crypto trading volume'),

    html.Br(),

    html.Label('Choose a cryptocurrency:'),
    dcc.Dropdown(
        id='crypto_drop',
        options=crypto_options,
        value='Bitcoin',
        multi=True
    ),

    dcc.Graph(id='grafico')
])

@app.callback(
    Output('grafico', 'figure'),
    [Input('crypto_drop', 'value')]
)


def update_graph(cryptos):
    scatter_data = []

    for crypto in cryptos:
        filtered_by_crypto_df = df.loc[df['crypto_name'] == crypto]

        temp_data = dict(
            type='scatter',
            y=filtered_by_crypto_df['volume'],
            x=filtered_by_crypto_df['year'],
            name=crypto
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Date'),
                          yaxis=dict(title='Trading Volume')
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)