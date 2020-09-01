from plotly import graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
import pickle
from flask import Flask

FigURL = "https://decovindia.s3.ap-south-1.amazonaws.com/figures"
#FigURL ="https://storage.googleapis.com/creditdecov/figures"

fig  = pickle.load(urlopen(FigURL))

colors ={}
colors['Borrowings']='rgb(139,48,88)'
colors['Restructurings']='rgb(25,51,80)'
colors['Repayments']='rgb(86,177,163)'


industries = ['Hotels','Restaurants','Air Transport','Water Transport','Land Transport',
                'Manufacturing of Allopathic Medicines','Manufacturing of Pharmaceutical Ingredients',
                'Manufacturing of Surgical Equipment','Retail Sale of Pharmaceuticals','Wholesale of Pharmaceuticals']
types      = ['Borrowings', 'Restructurings', 'Repayments']

###########################

server = Flask(__name__)
@server.route('/')

app    = dash.app(__name__,server=server)

app.layout = html.Div([
    html.H1("Corporate Credit dashboard",style={'text-align':'center',
                                                'font-family': 'lato',
                                                'font-size': '100%',
                                                'font-weight': 'bold'
                                               })    ,
    html.Div([
        html.Div([
            html.Label('industry_select'),
            dcc.Dropdown(
                 id = 'industry_select',
                options=[
                     {"label":"Manufacturing of Allopathic Medicines",
                      "value":"Manufacturing of Allopathic Medicines"},
                     {"label":"Manufacturing of Pharmaceutical Ingredients",
                      "value":"Manufacturing of Pharmaceutical Ingredients"},
                     {"label":"Manufacturing of Surgical Equipment",
                      "value":"Manufacturing of Surgical Equipment"},
                    {"label": "Retail Sale of Pharmaceuticals",
                     "value":"Retail Sale of Pharmaceuticals"},
                    {"label":"Wholesale of Pharmaceuticals",
                    "value":"Wholesale of Pharmaceuticals"},
                     {"label":"Land Transport",
                      "value":"Land Transport"},
                     {"label":"Air Transport",
                      "value":"Air Transport"},
                     {"label":"Water Transport",
                      "value":"Water Transport"},
                     {"label":"Hotels",
                      "value":"Hotels"},
                     {"label":"Restaurants",
                      "value":"Restaurants"}],
                multi = False,
                value = 'Land Transport'

                 ),
                ]),

        html.Div([

            html.Label('type_select'),
            dcc.Dropdown(
             id = 'type_select',
                 options=[
                     {"label":"Borrowings",
                      "value":"Borrowings"},
                     {"label":"Restructurings",
                      "value":"Restructurings"},
                     {"label":"Repayments",
                      "value":"Repayments"}],
                multi = False,
             value = 'Borrowings')
             ,
        ]),
            ]),

    dcc.Graph(id = 'graph')
    ])

@app.callback(Output('graph', 'figure'),
    [Input('industry_select', 'value'),
     Input('type_select', 'value')])
def update_graph(Industry, Type,fig=fig):
    return fig[Industry][Type]

if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port=8080, debug=True)
