import pandas as pd
import numpy as np
import plotly.express as px
import dash
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
    dcc.Dropdown(id = 'species', options = species_options,  multi=True, value = 'Black Cherry')
    ], style = {'width':'48%', 'display':'inline-block'})
])


if __name__ == '__main__':
    app.run_server()
