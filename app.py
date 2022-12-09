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
air_masuk1 = "Chart Inflow"

air_keluar1 = "Chart Outflow "

url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZ8z6itG8nQZD67jMNQzHY_AGwZy4hchWg7gv1YWwrm1wDV-MC2actFWNc09khWq9t_2aTep77k7My/pub?output=csv&sheet={air_masuk1}"
url_outflow = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQf-6x9UNzaLvMYnLobX3YxLvV8lhoWWzRDaO4I5ettKf3jZ_Z4a6rGYEL59CQ7GUmJGGs5hTeEPsD_/pub?output=csv&sheet={air_keluar1}"


df_masuk = pd.read_csv(url_inflow)
df_keluar = pd.read_csv(url_outflow)



#membangun komponen
header = html.Div([html.H1("Aplikasi Simulasi Kapasitas Embung F ITERA"), html.H3("Kelompok 4")],style={
    "textAlign" : "center",
    "height": "4 rem",
    "padding": "2rem 1rem",
    "background-color": "#FF99CC"
})





subtitle = html.Div([html.P("Embung F merupakan salah satu embung ITERA yang berfungsi menyimpan air hujan pada suatu kolam dan dioperasikan pada musim kering untuk berbagai kebutuhan air."),html.P("Data Embung F"),html.P("Luas = 0,56 Ha"),html.P("Volume = 19.600 m^3"),html.P("Pemanfaatan air embung merupakan fungsi dari inflow, outflow dan tampungan embung. Inflow adalah aliran sungai yang masuk ke embung. Outflow terdiri dari lepasan embung untuk irigasi, air baku dan kebutuhan konservasi sungai."), html.P("Permodelan simulasi tampungan embungan merupakan selisih nilai inflow dan nilai outflow.")],style={"height": "4 rem",
    "padding": "2rem 1rem","background-color": "#FFCCE5"})
datamasuk_gam = go.FigureWidget()
datamasuk_gam.add_bar(name="Chart Inflow", x=df_masuk['Waktu'], y=df_masuk['Data'] )
datamasuk_gam.layout.title = 'Chart Inflow Embung F'

datakeluar_gam = go.FigureWidget()
datakeluar_gam.add_scatter(name="Outflow " , x=df_keluar['Waktu'], y=df_keluar['Data'])
datakeluar_gam.layout.title = 'Chart Outflow Embung F'

simulation_fig = go.FigureWidget()
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle])  ,
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datamasuk_gam)] ),
               
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
        html.Div(id='output-container-button', children='Klik Run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
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
        inout1 =  (df_masuk['Data'].values - df_keluar['Data'].values)
        N = len(inout1)
        u = np.zeros(N)
        u0 = 19600
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout1[n] 
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_keluar['Waktu'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulasi Kapasitas Embung E ITERA '

        return simulation_fig


#jalankan aplikasi
if __name__=='__main__':
    app.run_server(debug=True, port=2022)

