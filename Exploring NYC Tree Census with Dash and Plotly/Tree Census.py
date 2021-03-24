import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html 

tree_health_by_boro_url = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json?' +\
        '$select=spc_common,boroname,steward,health,count(tree_id)' +\
        '&$group=spc_common,boroname,steward,health' +\
        '&$where=spc_common IS NOT NULL'.replace(' ', '%20') +\
        '&$limit=5000'

df = pd.read_json(tree_health_by_boro_url)
df['spc_common'] = df['spc_common'].str.title()

proportion = df.groupby('health')

app = dash.Dash()


boro_options = []
for boro in df['boroname'].unique():
    boro_options.append({'label':boro, 'value':boro})

species_options = []
for spec in df['spc_common'].unique():
    species_options.append({'label':spec, 'value':spec})


app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id = 'boro', options = boro_options,  multi=True, value = 'Brooklyn')],
        style = {'width':'48%', 'display':'inline-block'}), 
    html.Div([
        dcc.Dropdown(id = 'species', options = species_options,  multi=True, value = 'American Beech')
        ], style = {'width':'48%', 'display':'inline-block'}),
    html.Div(
        [dcc.Graph(id = 'graphic')], style = {'padding':10})
])

@app.callback(Output('graphic', 'figure'), [Input('boro', 'value'), Input('species', 'value')])
def update_graph(val_boro, val_species):
    filtered_df = df[(df['boroname']==val_boro) & (df['spc_common']==val_species)]
    grouped_df = filtered_df.groupby('health').sum()
    return px.bar(grouped_df, x = grouped_df.index, y = 'count_tree_id')

if __name__ == '__main__':
    app.run_server()
