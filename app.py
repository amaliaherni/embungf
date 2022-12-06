#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
air_masuk1 = "Chart Air Masuk "

air_keluar1 = "Chart Air Keluar "

url_masuk = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVE6RWRi3EG9vL2iBq7Vw2RK3SW2-iIwAaFus3nU2HLbbzhZ3Jb3xVdv6Kd-nJ-hu4gu8ftRZ4mJvF/pub?output=csv&sheet={air_masuk1}"
url_keluar = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQQVBtC-xGgAwkkTOMCEEJp78FbJTlBxWD39LXtRdRs9S5Pl4yjFjT7XZpGie1BgUpSrTVGgda74ste/pub?output=csv&sheet={air_keluar1}"


df_masuk = pd.read_csv(url_masuk)
df_keluar = pd.read_csv(url_keluar)



#membangun komponen
header = html.Div([html.H1("Aplikasi Simulasi Kapasitas Embung E ITERA"), html.H3("Kelompok 7")])

subtitle = html.P("Kelompok...",style={})

datamasuk_gam = go.FigureWidget()
datamasuk_gam.add_bar(name="Chart Air Masuk Pertama", x=df_masuk['Bulan'], y=df_masuk['Data-masuk'])

datamasuk_gam.layout.title = 'Chart Inflow Embung '

datakeluar_gam = go.FigureWidget()
datakeluar_gam.add_scatter(name="Outflow Pertama" , x=df_keluar['Bulan'], y=df_keluar['Data-keluar'])

datakeluar_gam.layout.title = 'Chart Outflow Embung'

simulation_fig = go.FigureWidget()
# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle])  ,
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datamasuk_gam)]),
               
            ]
            ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datakeluar_gam)]),
                
            ]
            ),
        html.Div(
            [
                dbc.Button('Run', color="warning",id='run-button', n_clicks=0)
            ],style = {'textAlign': 'center'})
        , 
        html.Div(id='output-container-button', children='Klik tombol "Run" untuk menjalankan .', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        )
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection
    if n_clicks >=1:
        #program numerik ---start----
        inout1 =  (df_masuk['jumlah'].values - df_keluar['jumlah'].values)
        N = len(inout1)
        u = np.zeros(N)
        u0 = 196800
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout1[n] 
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_keluar['Bulan'], y=u)
        simulation_fig.layout.title = 'Hasil Simulasi'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulasi Kapasitas Embung E ITERA '

        return simulation_fig

    


#jalankan aplikasi
if __name__=='__main__':
    app.run_server()

#debug=True, port=1191
